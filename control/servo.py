"""servo.py
Basic Servo Class to steer the boat
"""
from control import automatic_motor_control as AMC

class Servo():
    """
    Initialize Servo Object
    """

    def __init__(self, number, kit, is_back, max_move, min_move):
        self.kit = kit
        self.number = number
        self.is_back = is_back
        self.max_move = max_move
        self.min_move = min_move

    def reset(self):
        """
        Set servo to 0 degrees
        :return:
        """
        self.kit.servo[self.number].angle = self.max_move + self.min_move / 2

    def move(self, deg):
        """
        Move to the degree location (0 - 180).
        :param deg:
        :return:
        """
        try:
            deg = AMC.range_conversion(deg, 180, 0, self.max_move, self.min_move)
            self.kit.servo[self.number].angle = deg
        except ValueError:
            print("Bad Angle, passing.")

        # if self.max_move >= deg >= self.min_move:
        #     self.kit.servo[self.number].angle = deg
        # elif deg < self.min_move:
        #     self.kit.servo[self.number].angle = self.min_move
        # elif deg < self.max_move:
        #     self.kit.servo[self.number].angle = self.max_move
