import time
from machine import Pin
import dht
import network
import esp32
import urequests
import uasyncio as asyncio

ap_ssid = None
ap_key = None

wifi_id = None
wifi_key = None


def connect_to_wifi():
    global wlan
    wlan = network.WLAN(network.STA_IF)

    wlan.active(False)

    wlan.active(True)
    wlan.connect(wifi_id, wifi_key)


async def check_wifi_connection():
    try:
        if not wlan.isconnected():
            print("Connecting to Wifi...")
            wlan.connect(wifi_id, wifi_key)

            while not wlan.isconnected():
                await asyncio.sleep(1)

        print("Connected to Wifi:", wlan.ifconfig())

    except Exception as e:
        print("Exception in wifi check", e)


def read_sensor():
    timestamp_sensor = time.ticks_ms() / 1000

    try:
        sensor.measure()
        temp = sensor.temperature()
        esp_temp = esp32.raw_temperature()
        hum = sensor.humidity()
        esp_temp_celsius = (esp_temp - 32) / 1.8

        print("___")
        print("Temperature: %3.1f C" % temp)
        print("ESP32 Temperature: %3.1f C" % esp_temp_celsius)
        print("Humidity: %3.1f %%" % hum)

    except OSError as e:
        temp = 0
        print("Failed to read sensor.", e)

    return temp, timestamp_sensor


async def read_sensor_and_transmit():
    asyncio.create_task(check_wifi_connection())

    temperature, timestamp = read_sensor()
    data = {"temperature": temperature, "timestamp": timestamp}
    response = urequests.post(url, json=data, headers=headers)
    response.close()


data_pin = Pin(27)
sensor = dht.DHT11(data_pin)

# Connectivity parameters

global url, headers

url = None + "coffee"
headers = {"Content-Type": "application/json"}


async def main():
    connect_to_wifi()

    while True:
        # await check_wifi_connection()
        try:
            await read_sensor_and_transmit()
        except Exception as e:
            print("exceeption in main loop", e)

        await asyncio.sleep(2)  # 1000 ms


loop = asyncio.get_event_loop()
loop.create_task(main())
loop.run_forever()

# Todo: https://github.com/micropython/micropython/issues/5783