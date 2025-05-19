import json
import pika
from django.core.management.base import BaseCommand
from influxdb_client import InfluxDBClient, Point
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import os
import django
import time
from datetime import datetime, timedelta
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'APIRest.settings')
django.setup()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'APIRest.settings')
django.setup()

class Command(BaseCommand):
    help = 'Start MQTT consumer and forward to InfluxDB and WebSocket'

    def handle(self, *args, **kwargs):
        token = "To8XoxF9cnENPLcjhnTf12ll5EhON2N-1IES8YqZkNW2j01dSTgr7Sq_fzFvlG8a91CQbZx-pgNY7FFM8T5pcg=="
        org = "iot_org"
        bucket = "eletricSensor_data"

        influx_client = InfluxDBClient(url="http://localhost:8086", token=token, org=org)
        write_api = influx_client.write_api()
        last_message_time = datetime.now()
        channel_layer = get_channel_layer()
        print(get_channel_layer())


        def on_timeout():
            print("⏰ Timeout: Nenhuma mensagem recebida nos últimos 20 segundos.")
            async_to_sync(channel_layer.group_send)(
                "sensor_data",
                {
                    "type": "send_sensor_data",
                    "data": None
                }
            )

        def write_to_influxdb(data):
            try:
                point = (
                    Point("eletricSensorV2")
                    .field("voltage", data['voltage'])
                    .field("current", data['current'])
                    .field("power", data['power'])
                    .field("energy", data['energy'])
                    .field("frequency", data['frequency'])
                    .field("pf", data['pf'])
                )
                write_api.write(bucket=bucket, org=org, record=point)
                print("✅ Data written to InfluxDB")
            except Exception as e:
                print(f"❌ Error writing to InfluxDB: {e}")

        def callback(ch, method, properties, body):
            nonlocal last_message_time
            try:
                data = json.loads(body)
                print(f"📥 Received: {data}")
                if(data['current'] == 0 and data['power'] == 0):
                    async_to_sync(channel_layer.group_send)(
                        "sensor_data",
                        {
                            "type": "send_sensor_data",
                            "data": None
                        }
                    )
                else:
                    write_to_influxdb(data)
                    async_to_sync(channel_layer.group_send)(
                        "sensor_data",
                        {
                            "type": "send_sensor_data",
                            "data": data
                        }
                    )
                    print("📡 Sent to WebSocket")
                last_message_time = datetime.now()
            except Exception as e:
                print(f"❌ Callback error: {e}")

        print("📡 Connecting to RabbitMQ...")
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='eletricSensor')
        channel.basic_consume(queue='eletricSensor', on_message_callback=callback, auto_ack=True)

        print("🟢 Listening for messages. Press CTRL+C to stop.")
        try:
            while True:
                connection.process_data_events(time_limit=1)
                now = datetime.now()
                if (now - last_message_time) > timedelta(seconds=20):
                    on_timeout()
                    last_message_time = now  # resetar para evitar chamadas continuas
        except KeyboardInterrupt:
            print("🛑 Stopped.")
            channel.stop_consuming()
        finally:
            connection.close()
