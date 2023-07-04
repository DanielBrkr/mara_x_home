# mara_x_home

## Goal
This is the repository of my diy portafilter coffee machine IoT project. It's supposed to provide push notifications whether the coffee machine is up to speed - it takes quiet some time to reach the brewing temperature - and tell whether i forgot to switch it off after 2 hours.
This is also the basis for my next smarthome projects.

It's possibly the first project for the Lelit Mara X using a ESP32 with MicroPython (https://micropython.org/), a bare-metal version of Python for microcontrollers.


## Architecture
![Mara_x_home_arch](https://github.com/DanielBrkr/mara_x_home/assets/138571169/9ffa18e5-79e2-458e-a5c9-2c0ccd2bf803)


*RPI 4 = Raspberry Pi 4

## Project Structure

### Backend (µC and Database)

This is where the MicroPython code for the ESP32 resides "/backend/temp_readout_prototype/" and the regular Python code for the MQTT host, that is dealing with the received temperature readings and pushing them to a database. The MQTT host which subscribes to the topic "coffee" can run either on a PC or Raspberry Pi. 

### Frontend (Prototyping)

The frontend is, as illustrated by the figure, only optional, but it's quiet convenient for prototyping. I've explored two routes, the first one is via a flask server and the second one via the Reflex Framework (https://reflex.dev/), which is a new web app development framework in pure Python. 


### Next Steps

Setup a homebridge device to access the MQTT topic "coffee" and integrate the ESP32 with the Mara X.


