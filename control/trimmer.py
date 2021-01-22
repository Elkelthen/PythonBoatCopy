"""
This file should only be run manually right now. It should not be referenced
in the program. Allows us to set trim values and save them to a file for PWM
purposes in the main program.
"""

from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)

kit.servo[2].angle = 90
kit.servo[3].angle = 90
kit.servo[4].angle = 90
kit.servo[5].angle = 90

angle_list = []

while True:
    IN_VAL = input("Enter a motor and a degree: ")
    IN_VAL = IN_VAL.split()

    kit.servo[int(IN_VAL[0]) + 2].angle = int(IN_VAL[1])
    print("Moved Servo " + str(IN_VAL[0]) + " to " + str(IN_VAL[1]) + " degrees.")
