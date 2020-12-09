#!/bin/sh

#Start by giving admin access for this shell
sudo su

#Go to the right directory
cd /home/pi/Desktop/PythonBoat

#Have to run this or boatbrain won't start. Something to do with the Servos, I think,
#although it affects all of the GPIO.
sudo pigpiod

#Run the updater. We don't pull from git in bash because I don't know how and python is easy.
#NOTE: this won't actually run the latest copy of the updater, which is slightly annoying.
#      it only pulls from git, which may also include an (updated) updater. Hmph. We could
#      set up a server in the future, but that probablt isn't worth it for now.
/usr/bin/python3 Updater.py

#The updater pulls another copy of pythonboat. When I do this manually, the cli stays on the
#same directory, but doesn't have anything in that directory, since we had just deleted it.
#I'm not really sure this part is necessary, but it can't hurt and may solve a problem. So here it is.
cd /home/pi/Desktop/PythonBoat

#Start Boatbrain.
/usr/bin/python3 boat_brain.py

