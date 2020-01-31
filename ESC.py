import time
import pigpio

#1000 to calibrate. This should be done on startup.
#between 1150 and 2000(?) to control speed.


#Class to control VSDs through the use of ESCs.
class ESC():
    
    #initialize ESC Object
    def __init__(self, pin, pi):
        self.pi = pi
        self.pin = pin
        pi.set_servo_pulsewidth(pin, 0)
        
    #Reset ESC. This should be followed by a series of beeps. This is calibration.
    def reset(self):
        self.pi.set_servo_pulsewidth(self.pin, 1000)
    
    #Change Speed of VSD
    def setSpeed(self, speed):
        self.pi.set_servo_pulsewidth(self.pin, speed)