from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
import json
import aiohttp
from carregamentos.models import Carregamento
from postosCarregamento.models import PostoCarregamento
from utilizadores.models import Utilizador
from automoveis.models import Veiculo

# SensorDataConsumer (completo)
class SensorDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.session_id = None
        self.group_name = "sensor_data"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        print("🟢 WebSocket conectado")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        if self.session_id:
            await self.update_session_status('COMPLETED')
        print("🔴 WebSocket desconectado")

    async def receive(self, text_data):
        data = json.loads(text_data)

        if data.get('action') == 'start_charging':
            await self.handle_start_charging(data)
        elif data.get('action') == 'update_output':
            pass  # já lidas via RabbitMQ
        elif data.get('action') == 'charging_auto_ended':
            await self.handle_auto_end()
        elif data.get('action') == 'charging_stopped':
            await self.update_session_status('COMPLETED')

    async def handle_start_charging(self, data):
        vehicle = await self.get_vehicle(data['vehicle_id'])
        station = await self.get_charging_station(data['station_id'])
        user = await self.get_user(data['user_id'])

        if not station.pc_estado:
            return await self.send_error("Posto indisponível")

        self.session_id = await self.create_charging_session(station, user, vehicle)
        await self.send(json.dumps({'status': 'charging_started', 'session_id': self.session_id}))

        iot_url = station.pc_iot_equipamento.iot_url
        output_pin = station.pc_iot_equipamento.iot_output
        async with aiohttp.ClientSession() as session:
            await session.post(f"{iot_url}/start", json={"output_pin": output_pin})

    async def handle_auto_end(self):
        await self.send(json.dumps({'status': 'charging_auto_ended'}))

    async def send_sensor_data(self, event):
        await self.send(json.dumps({'status': 'charging_data', 'data': event['data']}))

    @database_sync_to_async
    def get_vehicle(self, vehicle_id): return Veiculo.objects.get(id=vehicle_id)

    @database_sync_to_async
    def get_charging_station(self, station_id): return PostoCarregamento.objects.select_related('pc_iot_equipamento').get(id=station_id)

    @database_sync_to_async
    def get_user(self, user_id): return Utilizador.objects.get(id=user_id)

    @database_sync_to_async
    def create_charging_session(self, station, user, vehicle):
        return Carregamento.objects.create(
            ca_utilizador=user, ca_posto=station, ca_entidade=station.pc_entidade,
            ca_carro=vehicle, ca_estado='ACTIVE'
        ).id

    @database_sync_to_async
    def update_session_status(self, status):
        if self.session_id:
            Carregamento.objects.filter(id=self.session_id).update(ca_estado=status)

    async def send_error(self, message):
        await self.send(json.dumps({'status': 'error', 'message': message}))
