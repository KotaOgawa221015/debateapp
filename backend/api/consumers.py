# whisper処理が必要になった時に使う想定
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import torch
import whisper

model = whisper.load_model("base")  # whisperモデル

class StreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, bytes_data=None, text_data=None):
        if bytes_data:
            # bytes → wav解析などの処理が必要（後で追加）
            result = model.transcribe(bytes_data)
            text = result.get("text", "")
            
            await self.send(json.dumps({
                "type": "final",
                "text": text
            }))
