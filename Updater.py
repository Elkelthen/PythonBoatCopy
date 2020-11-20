from git import Repo

repo = Repo('/home/pi/Desktop/PythonBoat')

repo.remotes.origin.pull()