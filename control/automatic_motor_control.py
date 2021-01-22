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

    # Convert to radians
    theta = theta * (math.pi / 180)

    # Find the correct thrust vector
    thrust_vector_x = math.cos(theta)
    thrust_vector_y = math.tan(theta)

    thrust_vector_x = thrust_vector_x * (180 / math.pi)
    thrust_vector_y = thrust_vector_y * (180 / math.pi)

    # Ensure a positive value for conversion in the next step.
    if thrust_vector_x < 0:
        thrust_vector_x += 360
    if thrust_vector_y < 0:
        thrust_vector_y += 360

    # Convert the thrust vector to a range of degrees.
    thrust_vector_x = range_conversion(thrust_vector_x, 360, 0, 180, 0)
    thrust_vector_y = range_conversion(thrust_vector_y, 360, 0, 180, 0)

    # Move the servos to the correct degree value.
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


def range_conversion(old_val, old_max, old_min, new_max, new_min):
    return (((old_val - old_min) * (new_max - new_min)) / (old_max - old_min)) + new_min
