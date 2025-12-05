import asyncio
import subprocess
import tempfile
import os
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# フロントからの接続を許可
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Whisper.cpp の実行ファイル
WHISPER_EXE = "whisper-server.exe"        # backend フォルダに置いてください
MODEL_PATH = "ggml-base.ja.bin"    # モデルファイルも backend に置く


def run_whisper(wav_path: str) -> str:
    """
    Whisper.cpp を一回実行して文字起こしする関数
    """
    cmd = [
        WHISPER_EXE,
        "-m", MODEL_PATH,
        "-f", wav_path,
        "--output-txt",  # result.txt を出力
        "-otxt"
    ]

    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Whisper.cpp は result.txt を出力する
    result_path = "result.txt"
    if os.path.exists(result_path):
        with open(result_path, "r", encoding="utf-8") as f:
            return f.read().strip()

    return ""


@app.websocket("/ws/stream")
async def websocket_stream(websocket: WebSocket):
    await websocket.accept()
    print("Client connected")

    buffer = b""                    # 音声バッファ
    MIN_CHUNK = 16000 * 1           # 約1秒（PCM 16bit の場合）

    try:
        while True:
            data = await websocket.receive_bytes()
            buffer += data

            # 音声が一定以上たまったら Whisper に渡す
            if len(buffer) >= MIN_CHUNK:
                # 一時ファイルに WAV 書き出し
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                    wav_path = tmp.name
                    tmp.write(buffer)     # ここではすでに PCM(WAV) 前提
                    tmp.flush()

                # Whisper に送る
                text = run_whisper(wav_path)

                # クライアントへ返す
                if text:
                    await websocket.send_text(text)

                # バッファをリセット
                buffer = b""

    except Exception as e:
        print("WebSocket Error:", e)

    finally:
        print("Client disconnected")
