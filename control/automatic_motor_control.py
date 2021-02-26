""""automatic_motor_control.py

This module contains no classes, only helper methods to help control
the speed and direction of the boats.

Accessed by boat_brain.py

"""

import math
import geopy.distance
import data_globals


def set_thrust_direction(current_heading, go_to_coords, current_coords, servo_x, servo_y):
    """setThrustDirection()

    Takes input from boat_brain.py to calculate the necessary position of servos for VSD control.

    """
    go_to_heading = (math.atan2(go_to_coords[1] - current_coords[1],
                                    go_to_coords[0] - current_coords[0]))

    data_globals.TARGET_HEADING_G = go_to_heading

    theta = (go_to_heading - current_heading) * (math.pi / 180) + (math.pi / 4)
    #adds 45 degrees to heading to correct for motor orientation

    # Find the correct thrust vector
    # Normalized between 0 and 1 (NOT degrees or radians)
    thrust_unit_vector_x = math.cos(theta)
    thrust_unit_vector_y = math.sin(theta)

    # Move the servos to the correct degree value.
    servo_x.move(thrust_unit_vector_x)
    servo_y.move(thrust_unit_vector_y)


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


def range_conversion(old_val, old_max, old_min, new_max, new_min):
    return (((old_val - old_min) * (new_max - new_min)) / (old_max - old_min)) + new_min
