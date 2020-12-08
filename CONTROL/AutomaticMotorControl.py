""""AutomaticMotorControl.py

This module contains no classes, only helper methods to help control
the speed and direction of the boats.

Accessed by BoatBrain.py

"""

import math
import geopy.distance


def setThrustDirection(currentHeading, goToCoords, currentCoords, servoX, servoY):
    """setThrustDirection()

    Takes input from BoatBrain.py to calculate the necessary position of servos for VSD control.

    """
    goToHeading = 180 * (math.atan2(goToCoords[1] - currentCoords[1],
                                    goToCoords[0] - currentCoords[0])) / math.pi

    theta = goToHeading - currentHeading

    theta = theta * (math.pi / 180)

    thrustVectorX = 30 * math.sin(theta)
    thrustVectorY = 30 * math.cos(theta)

    if thrustVectorX < 0:
        thrustVectorX += 90
    if thrustVectorY < 0:
        thrustVectorY += 90

    thrustVectorX = (((thrustVectorX - 0) * (115 - 75)) / (360 - 0)) + 75
    thrustVectorY = (((thrustVectorY - 0) * (115 - 75)) / (360 - 0)) + 75

    servoX.move(thrustVectorX)
    servoY.move(thrustVectorY)


def setThrustSpeed(goToCoords, currentCoords, esc):
    """setThrustSpeed()

    Takes input from BoatBrain.py to send a PWM signal to the ESC, determining speed.

    """

    distmeters = geopy.distance.distance(goToCoords, currentCoords).m

    if distmeters <= 10:
        output = 0
    else:
        output = 1

    # NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
    # output = (((output - 0) * (1 - -1)) / (100 - 0)) + -1

    esc.setSpeed(output)
