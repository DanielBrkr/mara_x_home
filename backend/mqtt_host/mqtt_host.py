import json
import paho.mqtt.client as mqtt
from sqlalchemy import create_engine, Column, Integer, Float, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import pytz

# Set up database connection
engine = create_engine("sqlite:///sensor_data.db")
Base = declarative_base()


class SensorData(Base):
    __tablename__ = "coffee"
    id = Column(Integer, primary_key=True)
    humidity = Column(Float)
    temperature = Column(Float)
    timestamp = Column(DateTime)


Session = sessionmaker(bind=engine)


# Set up MQTT client
def on_connect(client, userdata, flags, rc):
    """Connects to the coffee topic of the broker running on raspberry pi"""

    client.subscribe("coffee")
    print("Connected to MQTT broker with result code " + str(rc))


def on_message(client, userdata, msg):
    """"""
    data = json.loads(msg.payload.decode())
    session = Session()

    datetime.fromtimestamp(data["timestamp"])
    # overwrites the microcontrollers timestamp with the timestamp of mqtt message arrival
    tz = pytz.timezone("Europe/Berlin")
    time_now = datetime.now(tz)
    time_now_formatted = time_now.strftime("%H:%M:%S - %d.%m.%Y")

    sensor_data = SensorData(
        humidity=data["humidity"], temperature=data["temperature"], timestamp=time_now
    )
    print(
        f'Received following sensor data for topic "{msg.topic}": \n'
        f"Timestamp: {time_now_formatted} \n"
        f"Temperature: {sensor_data.temperature} °C \n"
        f"Humidity: {sensor_data.humidity} % \n"
        f"_____________________________________________________________"
    )

    session.add(sensor_data)
    session.commit()


Base.metadata.create_all(engine)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
broker_ip: str = None
client.connect(broker_ip, 1883)

# Start MQTT client loop
client.loop_forever()
