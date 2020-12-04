from git import Repo
import time
import RPi.GPIO as GPIO
import os

# A very simple class for updating the boat remotely.
# The idea is that we should be able to run the pi in
# headless mode, plugged into ethernet, and have it update
# correctly before running the actual Boatbrain.py program.

# This sets the pinmode to reference the numbers in the charts,
# not directly on the board. I do this because I'm a masochist.
GPIO.setmode(GPIO.BCM)

# Pin definitions. Each pin will correspond to a different branch in the repo.
Branch1 = 21
Branch2 = 20
Branch3 = 19

GPIO.setup(Branch1, GPIO.IN)
GPIO.setup(Branch2, GPIO.IN)
GPIO.setup(Branch3, GPIO.IN)

# Path to the local Repo on the pi. we start by removing the directory so that we can
# avoid merge conflicts and other things like that. Just doing a clean install should be fine.
if os.path.exists('/home/pi/Desktop/PythonBoat'):
    os.remove('/home/pi/Desktop/PythonBoat')

# These branches can be changed easily. Theoretically, we will never change
# The master branch pin definition (no pin at all), so we will always be able
# To push updated pin defs for new branches and update without having to actually
# go into the pi itself. There may be a better way to do this.
if GPIO.input(Branch1):
    Repo.clone_from("https://github.com/JFreyWM/PythonBoat.git", '/home/pi/Desktop/PythonBoat',
                    branch='JRG_Branch')

elif GPIO.input(Branch2):
    Repo.clone_from("https://github.com/JFreyWM/PythonBoat.git", '/home/pi/Desktop/PythonBoat',
                    branch='LSM9DS_IMU')

elif GPIO.input(Branch3):
    # We don't have a third branch yet,
    # just leaving it here so we can expand later.
    pass

else:
    # If we have no input to the Pi, just pull master (no branch defaults to master).
    Repo.clone_from("https://github.com/JFreyWM/PythonBoat.git", '/home/pi/Desktop/PythonBoat')

# Sleep for a few seconds just to avoid any problems transitioning into the boatBrain program.
# Remember, this script is called by start_boat.sh on startup.
time.sleep(5)
