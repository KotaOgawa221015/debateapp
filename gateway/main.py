# gateway/main.py
import asyncio
from fastapi import FastAPI, WebSocket
from whisper_wrapper import WhisperStream

app = FastAPI()

async def audio_chunks(ws):
    while True:
        try:
            data = await ws.receive_bytes()
        except:
            break
        yield data

@app.websocket("/ws/stream/")
async def stream(ws: WebSocket):
    await ws.accept()
    whisper = WhisperStream()

    async for chunk in audio_chunks(ws):
        text = whisper.feed_audio(chunk)
        if text:
            await ws.send_json({"type": "partial", "text": text})

    whisper.close()
