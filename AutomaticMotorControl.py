import math
import geopy.distance
from simple_pid import PID

def setThrustDirection(currentHeading, goToCoordsY, goToCoordsX, latitude, longitude, ServoX, ServoY):
    goToHeading = 180 * (math.atan2(goToCoordsY - longitude, goToCoordsX - latitude)) / math.pi

    theta = goToHeading - currentHeading

    theta = theta * (math.pi / 180)

    thrustVectorX = 30 * math.sin(theta)
    thrustVectorY = 30 * math.cos(theta)

    if thrustVectorX < 0:
        thrustVectorX += 360
    if thrustVectorY < 0:
        thrustVectorY += 360

    thrustVectorX = (((thrustVectorX - 0) * (115 - 75)) / (360 - 0)) + 75
    thrustVectorY = (((thrustVectorY - 0) * (115 - 75)) / (360 - 0)) + 75

    ServoX.move(thrustVectorX)
    ServoY.move(thrustVectorY)

def setThrustSpeed(goToCoordsY, goToCoordsX, pid, longitude, latitude, ESC):

    coords1 = (goToCoordsX, goToCoordsY)
    coords2 = (latitude, longitude)

    distmeters = geopy.distance.distance(coords1, coords2).m

    if distmeters <= 10:
        output = 0
    else:
        output = 1

    #NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
    #output = (((output - 0) * (1 - -1)) / (100 - 0)) + -1

    ESC.setSpeed(output)
