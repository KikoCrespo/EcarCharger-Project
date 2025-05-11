import os
import django
import pika
import json
from influxdb_client import InfluxDBClient, Point
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Setup Django context
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "APIRest.settings")
django.setup()

# InfluxDB config
INFLUX_TOKEN = "To8XoxF9cnENPLcjhnTf12ll5EhON2N-1IES8YqZkNW2j01dSTgr7Sq_fzFvlG8a91CQbZx-pgNY7FFM8T5pcg=="
INFLUX_ORG = "iot_org"
INFLUX_BUCKET = "eletricSensor_data"
INFLUX_URL = "http://localhost:8086"

influx_client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = influx_client.write_api()

def write_to_influxdb(data):
    point = (
        Point("eletricSensorV2")
        .field("voltage", data["voltage"])
        .field("current", data["current"])
        .field("power", data["power"])
        .field("energy", data["energy"])
        .field("frequency", data["frequency"])
        .field("pf", data["pf"])
    )
    write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)
    print("[InfluxDB] Data written")


def callback(ch, method, properties, body):
    print("📥 Recebida nova mensagem do RabbitMQ")
    try:
        data = json.loads(body)
        print(f"✅ Dados decodificados: {data}")


        # Save to InfluxDB
        write_to_influxdb(data)

        # Send via WebSocket to Django Channels
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "sensor_group",  # Nome do grupo
            {
                "type": "send_sensor_data",
                "data": data
            }
        )
    except Exception as e:
        print(f"Error: {e}")


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='eletricSensor')

    channel.basic_consume(queue='eletricSensor', on_message_callback=callback, auto_ack=True)

    print("[*] Waiting for messages...")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
        connection.close()


if __name__ == '__main__':
    main()