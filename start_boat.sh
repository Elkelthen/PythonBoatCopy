#!/bin/sh

cd /home/pi/Desktop/PythonBoat

sudo pigpiod

/usr/bin/python3 Updater.py

/usr/bin/python3 BoatBrain.py

