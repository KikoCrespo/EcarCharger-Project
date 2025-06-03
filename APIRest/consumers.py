from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.core.exceptions import ObjectDoesNotExist
import json
import aiohttp
from django.utils import timezone
from carregamentos.models import Carregamento
from postosCarregamento.models import PostoCarregamento
from utilizadores.models import Utilizador
from automoveis.models import Veiculo
from influxdb_client import InfluxDBClient

class SensorDataConsumer(AsyncWebsocketConsumer):
    # Connection Management
    async def connect(self):
        await self.accept()
        self.session_id = None
        self.group_name = "sensor_data"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        print("🟢 WebSocket conectado")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        print("🔴 WebSocket desconectado")

    # Message Routing
    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            action = data.get('action')

            if action == 'sensor_data':
                # Dados vindos do dispositivo IoT
                await self.handle_sensor_data(data)
            else:
                handler = getattr(self, f'handle_{action}', None)
                if handler:
                    await handler(data)
                else:
                    await self.send_error(f"Ação desconhecida: {action}")
        except json.JSONDecodeError:
            await self.send_error("Formato de dados inválido")
        except Exception as e:
            print(f"⚠️ Erro inesperado: {e}")
            await self.send_error("Erro interno no servidor")

    # Handlers
    async def handle_send_sensor_data(self, data):
        """Processa dados do sensor e envia para frontend"""
        session_id = data.get('session_id')
        payload = data.get('payload', {})

        if session_id:
            # Armazena o ID da sessão para referência
            if not self.session_id:
                self.session_id = session_id

            # Envia para o frontend
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "send.sensor.data",
                    "data": payload
                }
            )

    async def handle_start_charging(self, data):
        """Inicia nova sessão de carregamento"""
        station = await self.get_charging_station(data['station_id'])
        if not station.pc_estado:
            return await self.send_error("Posto indisponível")

        await self.update_charging_station_status(station.id, False)

        self.session_id = await self.create_charging_session(
            station,
            await self.get_user(data['user_id']),
            await self.get_vehicle(data['vehicle_id'])
        )

        await self.send(json.dumps({
            'status': 'charging_started',
            'session_id': self.session_id
        }))

        # Acionar dispositivo IoT
        iot = station.pc_iot_equipamento
        async with aiohttp.ClientSession() as session:
            await session.post(f"{iot.iot_url}/start", json={"output_pin": iot.iot_output})

    async def handle_resume_charging(self, data):
        """Retoma sessão existente"""
        try:
            session = await self.get_charging_session(data['session_id'])
            if session.ca_estado != 1:  # 1=EM_ANDAMENTO
                return await self.send_error("Sessão já concluída")

            self.session_id = session.id

            # Enviar apenas status da sessão, não os dados
            await self.send(json.dumps({
                'status': 'session_resumed',
                'session_id': self.session_id,
                'start_time': session.ca_data_inicio.isoformat()
            }))

        except ObjectDoesNotExist:
            await self.send_error("Sessão não encontrada")

    async def handle_charging_auto_ended(self, data):
        """Disparado quando IoT para de enviar dados"""
        # Registrar a data de fim imediatamente quando detecta paragem automática
        if self.session_id:
            await self.update_session_end_time(self.session_id)
            print(f"🕒 Data de fim registrada para sessão {self.session_id}")

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "send.auto.end",
            }
        )

    async def handle_confirm_auto_end(self, data):
        """Confirmação front-end com dados finais"""
        if not self.session_id:
            return

        # Receber a data de fim do frontend
        end_time_str = data.get('end_time')
        if not end_time_str:
            return await self.send_error("Data de fim não fornecida")

        try:
            from django.utils.dateparse import parse_datetime
            end_time = parse_datetime(end_time_str)
            if not end_time:
                return await self.send_error("Formato de data inválido")
        except Exception:
            return await self.send_error("Erro ao processar data de fim")

        # Buscar dados do InfluxDB para esta sessão
        session = await self.get_charging_session(self.session_id)

        station_id = await self.get_station_by_session(session.id)
        await self.update_charging_station_status(station_id, True)

        session_data = await self.get_session_data_from_influx(
            self.session_id,
            session.ca_data_inicio,
            end_time
        )

        # Finalizar sessão com os dados calculados e a data de fim correta

        await self.finalize_session(
            self.session_id,
            auto_stop=True,
            session_data=session_data,
            end_time=end_time
        )

        # Enviar resumo para o frontend
        await self.send(json.dumps({
            'status': 'session_summary',
            'session_id': self.session_id,
            'summary': session_data
        }))

    async def handle_charging_stopped(self, data):
        """Parada manual pelo usuário"""
        if not self.session_id:
            return

        # Buscar dados do InfluxDB para esta sessão
        session = await self.get_charging_session(self.session_id)

        station_id = await self.get_station_by_session(session.id)
        await self.update_charging_station_status(station_id, True)

        session_data = await self.get_session_data_from_influx(
            self.session_id,
            session.ca_data_inicio,
            session.ca_data_fim if session.ca_data_fim else timezone.now()
        )


        # Finalizar sessão com os dados calculados
        await self.finalize_session(
            self.session_id,
            auto_stop=False,
            session_data=session_data
        )

        await self.stop_charging_station(self.session_id)

        # Enviar resumo para o frontend
        await self.send(json.dumps({
            'status': 'session_summary',
            'session_id': self.session_id,
            'summary': session_data
        }))



    # IoT Control
    async def stop_charging_station(self, session_id):
        """Envia comando de parada para o posto"""
        iot_info = await self.get_iot_info(session_id)
        if not iot_info:
            return

        async with aiohttp.ClientSession() as session:
            await session.post(
                f"{iot_info['iot_url']}/stop",
                json={"output_pin": iot_info['output_pin']}
            )

    # Data Processing
    @database_sync_to_async
    def get_session_data_from_influx(self, session_id, start_time, end_time):
        """Busca dados da sessão no InfluxDB e calcula médias"""
        try:
            # Configuração do InfluxDB
            token = "To8XoxF9cnENPLcjhnTf12ll5EhON2N-1IES8YqZkNW2j01dSTgr7Sq_fzFvlG8a91CQbZx-pgNY7FFM8T5pcg=="
            org = "iot_org"
            bucket = "eletricSensor_data"

            client = InfluxDBClient(url="http://85.241.134.65:8086", token=token, org=org)
            query_api = client.query_api()

            # Usar end_time fornecido ou o momento atual
            if end_time is None:
                end_time = timezone.now()

            # Construir query para buscar dados da sessão
            query = f'''
            from(bucket: "{bucket}")
              |> range(start: {start_time.isoformat()}, stop: {end_time.isoformat()})
              |> filter(fn: (r) => r._measurement == "eletricSensorV2")
              |> mean()
            '''

            # Executar query
            result = query_api.query(query)

            # Processar resultados
            avg_voltage = 0
            avg_current = 0
            avg_power = 0
            avg_energy = 0

            for table in result:
                for record in table.records:
                    if record.get_field() == "voltage":
                        avg_voltage = record.get_value()
                    elif record.get_field() == "current":
                        avg_current = record.get_value()
                    elif record.get_field() == "power":
                        avg_power = record.get_value()
                    elif record.get_field() == "energy":
                        avg_energy = record.get_value()

            # Calcular duração
            duration = (end_time - start_time).total_seconds()

            # Calcular energia total (kWh)
            energy_consumed = avg_power * duration / 3600

            return {
                "avg_voltage": avg_voltage,
                "avg_current": avg_current,
                "avg_power": avg_power,
                "duration": duration,
                "energy_consumed": energy_consumed
            }

        except Exception as e:
            print(f"Erro ao buscar dados do InfluxDB: {e}")
            return {
                "avg_voltage": 0,
                "avg_current": 0,
                "avg_power": 0,
                "duration": 0,
                "energy_consumed": 0
            }


    @database_sync_to_async
    def finalize_session(self, session_id, auto_stop, session_data, end_time=None):
        """Finaliza sessão com cálculos finais"""
        try:
            session = Carregamento.objects.get(id=session_id)

            # Usar a data de fim fornecida ou o momento atual
            final_end_time = end_time or timezone.now()

            # Usar dados calculados do InfluxDB
            voltage = session_data["avg_voltage"]
            current = session_data["avg_current"]
            power = session_data["avg_power"]
            duration = session_data["duration"]
            energy_consumed = session_data["energy_consumed"]

            # Calcular custo
            custo = energy_consumed * session.ca_posto.pc_preco_kwh

            # Atualizar metadados
            session.ca_data_fim = final_end_time
            session.ca_duracao = duration
            session.ca_avg_v = voltage
            session.ca_avg_a = current
            session.ca_avg_kwh = power
            session.ca_custo = custo

            # Estado só muda em parada manual
            if not auto_stop:
                session.ca_estado = 2  # COMPLETED

            session.save()
            return True
        except ObjectDoesNotExist:
            return False

    # Database Operations
    @database_sync_to_async
    def get_charging_station(self, station_id):
        return PostoCarregamento.objects.select_related('pc_iot_equipamento').get(id=station_id)

    @database_sync_to_async
    def get_user(self, user_id):
        return Utilizador.objects.get(id=user_id)

    @database_sync_to_async
    def get_vehicle(self, vehicle_id):
        return Veiculo.objects.get(id=vehicle_id)

    @database_sync_to_async
    def get_charging_session(self, session_id):
        return Carregamento.objects.get(id=session_id)

    @database_sync_to_async
    def get_station_by_session(self, session_id):
        """Busca o posto de carregamento associado a uma sessão"""
        try:
            session = Carregamento.objects.get(id=session_id)
            return session.ca_posto.id
        except ObjectDoesNotExist:
            return None

    @database_sync_to_async
    def update_charging_station_status(self, station_id, status):
        """Atualiza o estado do posto de carregamento"""
        try:
            station = PostoCarregamento.objects.get(id=station_id)
            station.pc_estado = status
            station.save(update_fields=['pc_estado'])
            return True
        except ObjectDoesNotExist:
            return False

    @database_sync_to_async
    def create_charging_session(self, station, user, vehicle):
        return Carregamento.objects.create(
            ca_utilizador=user,
            ca_posto=station,
            ca_entidade=station.pc_entidade,
            ca_Veiculo=vehicle,
            ca_data_inicio=timezone.now(),
        ).id

    @database_sync_to_async
    def get_iot_info(self, session_id):
        try:
            session = Carregamento.objects.select_related(
                'ca_posto__pc_iot_equipamento'
            ).get(id=session_id)

            return {
                "iot_url": session.ca_posto.pc_iot_equipamento.iot_url,
                "output_pin": session.ca_posto.pc_iot_equipamento.iot_output
            }
        except ObjectDoesNotExist:
            return None

    @database_sync_to_async
    def update_session_end_time(self, session_id):
        """Atualiza apenas a data de fim da sessão"""
        try:
            session = Carregamento.objects.get(id=session_id)
            session.ca_data_fim = timezone.now()
            session.save(update_fields=['ca_data_fim'])
            return True
        except ObjectDoesNotExist:
            return False

    # Utilities
    async def send_sensor_data(self, event):
        """Envia dados do sensor para o frontend"""
        await self.send(json.dumps({
            'status': 'charging_data',
            'data': event['data']
        }))

    async def send_auto_ended(self, event):
        await self.send(json.dumps({
            'status': 'charging_auto_ended'
        }))

    async def send_error(self, message):
        await self.send(json.dumps({
            'status': 'error',
            'message': message
        }))
