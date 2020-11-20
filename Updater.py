from git import Repo


#A very simple class for updating the boat remotely.
#The idea is that we should be able to run the pi in
#headless mode, plugged into ethernet, and have it update
#correctly before running the actual Boatbrain.py program.

try:
    repo = Repo('/home/pi/Desktop/PythonBoat')
    repo.remotes.origin.pull()
except Exception as e:
    print(str(e))

