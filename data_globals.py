"""
This file contains all of the global variables used in the program
to help avoid cyclical dependencies.
"""
# Variables
ACC_G = 0
HEADING_G = 0
HEADING_FILTERED_G = [0] * 300
TARGET_HEADING_G = 0
H

# (Long, Lat) (X, Y)
CURRENT_LAT_LONG_G = [10, 10]
TARGET_LAT_LONG_G = [37.269, -76.716]
HOME_G = [0,0]

SERVO_ANGLES_G = [0, 0, 0, 0]

# Flags
NEW_INFO_F = False

SHUTDOWN_F = False

SET_HOME_F = False

GO_HOME_F = False

HOMED_G = False
