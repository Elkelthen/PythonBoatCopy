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

for i in range(4):
    for j in range(2):
        kit.servo[i + 2].angle = 90
        angle = 90
        IN_KEY = None
        while IN_KEY != 'l':
            IN_KEY = input(
                "Servo " + str(i) +
                " endpoint " + str(j) +
                " angle is " + str(angle) +
                "currently. use 'W' and 'S' "
                "to change the angle. when "
                "finished, press 'l' to save "
                "the value.")
            if IN_KEY.lower() == 'w':
                angle += 1
                kit.servo[i + 2].angle = angle
            elif IN_KEY.lower() == 's':
                angle -= 1
                kit.servo[i + 2].angle = angle
            else:
                continue
        angle_list.append(angle)

    print("Servo " + str(i) + " saved at " + str(angle) + " degrees. Going to next.")

print("Saving to file /home/pi/Desktop/PythonBoat/control/trimmed_values.txt")
file = open('/home/pi/Desktop/PythonBoat/control/trimmed_values.txt')
for i in angle_list:
    file.write(str(i))
file.close()
print("Saved. Exiting.")
