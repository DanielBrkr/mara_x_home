import time
import network
import ujson
import dht
import machine
import ubinascii
import uasyncio as asyncio
from umqtt.robust import MQTTClient


"""MQTT """
# Set up MQTT client
mqtt_client_id = ubinascii.hexlify(machine.unique_id()).decode("utf-8")
mqtt_topic = b"coffee"
mqtt_qos = 1
mqtt_user = ""
mqtt_password = ""

# MQTT parameters
mqtt_broker = None
mqtt_port = 1883

mqtt_client = MQTTClient(
    mqtt_client_id, mqtt_broker, user=mqtt_user, password=mqtt_password
)


# Set up DHT11 sensor
data_pin = machine.Pin(27)
sensor = dht.DHT11(data_pin)

# Set up Wi-Fi connection
wifi_id = None
wifi_key = None

wlan = network.WLAN(network.STA_IF)

# Set up HTTP request headers
headers = {"Content-Type": "application/json"}


# Connect to Wi-Fi
async def connect_to_wifi():
    global wlan
    wlan.active(False)
    wlan.active(True)
    time.sleep(0.1)
    wlan.connect(wifi_id, wifi_key)
    await asyncio.sleep(5)


# Check Wi-Fi connection
async def check_wifi_connection():
    try:
        while not wlan.isconnected():
            print("Connecting to Wi-Fi...")
            await connect_to_wifi()
            # await asyncio.sleep(5)

        print("Connected to Wi-Fi:", wlan.ifconfig())

    except Exception as e:
        print("Exception in Wi-Fi check", e)


# Read sensor data and transmit it over MQTT
async def read_sensor_and_transmit():
    try:
        # Read sensor data
        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity()
        timestamp = time.time()
        try:
            # Publish data to MQTT broker
            mqtt_client.connect()
            mqtt_client.publish(
                mqtt_topic,
                ujson.dumps(
                    {
                        "temperature": temperature,
                        "humidity": humidity,
                        "timestamp": timestamp,
                    }
                ),
                qos=mqtt_qos,
            )
            print("MQTT connection active")
            mqtt_client.disconnect()
        except OSError as e:
            print("Excepetion during mqtt communication", e)

    except Exception as e:
        print("Exception in sensor read and transmit", e)


# Main loop
async def main():
    while True:
        try:
            await check_wifi_connection()
            await read_sensor_and_transmit()
        except Exception as e:
            print("Exception in main loop", e)
        await asyncio.sleep(2)


loop = asyncio.get_event_loop()
loop.create_task(main())
loop.run_forever()

# ToDo: https://github.com/micropython/micropython-lib