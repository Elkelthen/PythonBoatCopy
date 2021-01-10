"""
Class for thruster.
currently only a logical distinction, nothing is really offered by having it set up this way.
"""
from control.servo import Servo
from control.esc import ESC


class Thruster:
    """
    Thruster Module contains 2 servos (x and y) and an ESC for speed control.
    """

    def __init__(self, kit, esc, servo_x, servo_y, max_move_1, min_move_1, max_move_2, min_move_2):
        """
        init. Needs to be refactored to remove some arguments or make them tuples.
        :param kit:
        :param esc:
        :param servo_x:
        :param servo_y:
        :param max_move_1:
        :param min_move_1:
        :param max_move_2:
        :param min_move_2:
        """
        self.motor_control_x = Servo(servo_x, kit, False, max_move_1, min_move_1)
        self.motor_control_y = Servo(servo_y, kit, False, max_move_2, min_move_2)
        self.esc = ESC(esc, kit)

        self.calibrate()

    def calibrate(self):
        """
        Reset for the beginning of a run.
        :return:
        """
        self.motor_control_x.reset()
        self.motor_control_y.reset()
        self.esc.reset()
