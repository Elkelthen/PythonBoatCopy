"""Servo.py
Basic Servo Class to steer the boat
"""


class Servo():
    """
    Initialize Servo Object
    """

    def __init__(self, number, kit, isBack):
        self.kit = kit
        self.number = number
        self.isBack = isBack

    def reset(self):
        """
        Set servo to 0 degrees
        :return:
        """
        self.kit.servo[self.number].angle = 0

    def move(self, deg):
        """
        Move to the degree location (0 - 180).
        :param deg:
        :return:
        """
        if self.isBack:
            self.kit.servo[self.number].angle = 95
        else:
            self.kit.servo[self.number].angle = deg
