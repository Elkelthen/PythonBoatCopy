from adafruit_servokit import ServoKit

#1000 to calibrate. This should be done on startup.
#between 1150 and 2000(?) to control speed.


#Class to control VSDs through the use of ESCs.
class ESC():
    
    #initialize ESC Object
    def __init__(self, pin, kit):
        self.kit = kit
        self.pin = pin
        
    #Reset ESC. This should be followed by a series of beeps. This is calibration.
    def reset(self):
        self.kit.continuous_servo[self.pin].throttle = -1
    
    #Change Speed of VSD
    def setSpeed(self, speed):
        self.kit.continuous_servo[self.pin].throttle = speed
