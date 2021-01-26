"""servo.py
Basic Servo Class to steer the boat
"""
from control import automatic_motor_control as AMC
import data_globals

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
        self.center = ((max_move - min_move) / 2) + min_move

    def reset(self):
        """
        Set servo to 0 degrees
        :return:
        """
        self.kit.servo[self.number].angle = (self.max_move - self.min_move) / 2 + self.min_move

    def move(self, unit_vector):
        """
        Move to the degree location (0 - 180).
        :param unit_vector:
        :return:
        """
        try:
            unit_vector = unit_vector * (self.max_move - self.center) + self.center
            #print('\n\n')
            #print(self.number, unit_vector)

            if unit_vector < self.min_move:
                self.kit.servo[self.number].angle = self.min_move
            elif unit_vector > self.max_move:
                self.kit.servo[self.number].angle = self.max_move
            else:
                self.kit.servo[self.number].angle = unit_vector

            data_globals.SERVO_ANGLES_G[self.number] = self.kit.servo[self.number].angle
        except ValueError:
            print("Bad Angle, passing.")

        # if self.max_move >= deg >= self.min_move:
        #     self.kit.servo[self.number].angle = deg
        # elif deg < self.min_move:
        #     self.kit.servo[self.number].angle = self.min_move
        # elif deg < self.max_move:
        #     self.kit.servo[self.number].angle = self.max_move
