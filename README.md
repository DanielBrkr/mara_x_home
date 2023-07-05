# mara_x_home

## Goal
This is the repository of my diy portafilter coffee machine IoT project. It's supposed to provide push notifications whether the coffee machine is up to speed - it takes quite some time to reach the brewing temperature - and tell whether i forgot to switch it off after 2 hours.
This is also the basis for my next smarthome projects.


## Architecture
![Mara_x_home_arch](https://github.com/DanielBrkr/mara_x_home/assets/138571169/9c74989e-e923-45b8-8735-589a38c9557e)



*RPI 4 = Raspberry Pi 4

## Project Structure

### Backend (µC and Database)

This is where the MicroPython code for the ESP32 resides "/backend/temp_readout_prototype/" and the regular Python code for the MQTT host, that is dealing with the received temperature readings and pushing them to a database. The MQTT host which subscribes to the topic "coffee" can run either on a PC or Raspberry Pi. 

### Frontend (Prototyping)

The frontend is, as illustrated by the figure, only optional, but it's quiet convenient for prototyping. I've explored two routes, the first one is via a flask server and the second one via the Reflex Framework (https://reflex.dev/), which is a new web app development framework in pure Python. 

#### Reflex Frontend

This is what the front facing page looks like, there will be a lot more temperatures to monitor when the ESP32 is actually connected to the coffee machine.

![grafik](https://github.com/DanielBrkr/mara_x_home/assets/138571169/eba57b2f-66db-4fe3-95a7-dc81cc455139)


If you run reflex for the first time you have to init it in the folder of reflex, like so:

```Python 
\mara_x_home\frontend\reflex_fe> reflex init
```

After you did that once, you can run it straight away via "reflex run":

```Python
\mara_x_home\frontend\reflex_fe> reflex run
```


### Next Steps

Setup a homebridge device to access the MQTT topic "coffee" and integrate the ESP32 with the Mara X.


