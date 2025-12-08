import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class AudioConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        if bytes_data:
            text = await self.transcribe(bytes_data)
            await self.send(json.dumps({"type": "final", "text": text}))

    async def transcribe(self, audio_bytes):
        response = client.audio.transcriptions.create(
            file=("audio.webm", audio_bytes, "audio/webm"),
            model="whisper-1",
        )
        return response.text
