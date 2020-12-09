""""automatic_motor_control.py

This module contains no classes, only helper methods to help control
the speed and direction of the boats.

Accessed by boat_brain.py

"""

import math
import geopy.distance


def set_thrust_direction(current_heading, go_to_coords, current_coords, servo_x, servo_y):
    """setThrustDirection()

    Takes input from boat_brain.py to calculate the necessary position of servos for VSD control.

    """
    go_to_heading = 180 * (math.atan2(go_to_coords[1] - current_coords[1],
                                    go_to_coords[0] - current_coords[0])) / math.pi

    theta = go_to_heading - current_heading

    theta = theta * (math.pi / 180)

    thrust_vector_x = 30 * math.sin(theta)
    thrust_vector_y = 30 * math.cos(theta)

    if thrust_vector_x < 0:
        thrust_vector_x += 90
    if thrust_vector_y < 0:
        thrust_vector_y += 90

    thrust_vector_x = (((thrust_vector_x - 0) * (115 - 75)) / (360 - 0)) + 75
    thrust_vector_y = (((thrust_vector_y - 0) * (115 - 75)) / (360 - 0)) + 75

    servo_x.move(thrust_vector_x)
    servo_y.move(thrust_vector_y)


def set_thrust_speed(go_to_coords, current_coords, esc):
    """setThrustSpeed()

    Takes input from boat_brain.py to send a PWM signal to the ESC, determining speed.

    """

    distmeters = geopy.distance.distance(go_to_coords, current_coords).m

    if distmeters <= 10:
        output = 0
    else:
        output = 1

    # NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
    # output = (((output - 0) * (1 - -1)) / (100 - 0)) + -1

    esc.set_speed(output)
