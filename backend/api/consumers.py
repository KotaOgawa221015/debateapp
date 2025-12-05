import json
from channels.generic.websocket import AsyncWebsocketConsumer

class StreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print("WebSocket Connected")

    async def disconnect(self, close_code):
        print("WebSocket Disconnected")

    async def receive(self, text_data=None, bytes_data=None):
        # 今はただ受け取ったデータを返すだけ（動作確認用）
        await self.send(json.dumps({
            "type": "final",
            "text": "受信しました"
        }))
