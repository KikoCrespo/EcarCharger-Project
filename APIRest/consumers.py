from channels.generic.websocket import AsyncWebsocketConsumer
import json

class SensorDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("sensor_data", self.channel_name)
        await self.accept()
        print("🟢 WebSocket conectado")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("sensor_data", self.channel_name)
        print("🔴 WebSocket desconectado")

    async def receive(self, text_data):
        print(f"🔵 Mensagem recebida do cliente: {text_data}")

    async def send_sensor_data(self, event):
        print(f"🟡 Enviando dados para cliente: {event['data']}")
        await self.send(text_data=json.dumps(event["data"]))
