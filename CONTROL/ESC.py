"""ESC.py

Lower level control functions for the speed control of the boat.

"""


#Class to control VSDs through the use of ESCs.
class ESC():
    """ESC()

    Electronic Speed controller class. Two of these
    are initialized, one for the front ESC, one for the back.

    """
    #initialize ESC Object
    def __init__(self, pin, kit):
        self.kit = kit
        self.pin = pin


    def reset(self):
        """
        Reset ESC. This should be followed by a series of beeps. This is calibration.
        :return:
        """
        self.kit.continuous_servo[self.pin].throttle = -1


    def setSpeed(self, speed):
        """
        Change Speed of VSD
        :param speed:
        :return:
        """
        self.kit.continuous_servo[self.pin].throttle = speed
