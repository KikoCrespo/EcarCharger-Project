'''from channels.generic.websocket import AsyncWebsocketConsumer
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
        await self.send(text_data=json.dumps(event["data"])) '''

# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.db import transaction
import json
import aiohttp
from carregamentos.models import Carregamento
from postosCarregamento.models import PostoCarregamento
from utilizadores.models import Utilizador
from automoveis.models import Veiculo

class SensorDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.session_id = None
        print("🟢 WebSocket conectado")

    async def disconnect(self, close_code):
        if self.session_id:
            await self.update_session_status('COMPLETED')
        print("🔴 WebSocket desconectado")

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)

            if data.get('action') == 'start_charging':
                await self.handle_start_charging(data)

            elif data.get('action') == 'update_output':
                await self.handle_output_update(data)

        except Exception as e:
            print(f"Erro: {str(e)}")
            await self.send_error(str(e))

    async def handle_start_charging(self, data):
        #device_data = data.get('iot_device')
        vehicle_id = data.get('vehicle_id')
        vehicle = Veiculo.objects.get(id=vehicle_id)
        station_id = data.get('station_id')
        station = PostoCarregamento.objects.get(id=station_id)
        user_id = data.get('user_id')
        user = Utilizador.objects.get(id=user_id)
        iot_device = station.pc_iot_equipamento

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                        f"{iot_device}/send-data",
                        json={'output_pin': station.pc_iot_equipamento}
                ) as response:
                    result = await response.json()

                    if response.status == 200:
                        self.session_id = await self.create_charging_session(
                            station, user, vehicle)
                        await self.send(json.dumps({
                            'status': 'charging_started',
                            'session_id': self.session_id
                        }))
                    else:
                        await self.send_error(result.get('error'))

            except Exception as e:
                await self.send_error(f"Connection error: {str(e)}")

    @database_sync_to_async
    def create_charging_session(self, station, user, vehicle):
        with transaction.atomic():

            session = Carregamento.objects.create(
                ca_utilizador=user,
                ca_posto=station,
                ca_estado='ACTIVE',
                ca_entidade=station.pc_entidade,
                ca_carro=vehicle,
            )
            return session.id

    @database_sync_to_async
    def update_session_status(self, status):
        Carregamento.objects.filter(id=self.session_id).update(status=status)

    async def send_error(self, message):
        await self.send(json.dumps({
            'status': 'error',
            'message': message
        }))