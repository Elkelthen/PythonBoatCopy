from adafruit_servokit import ServoKit


#Basic Servo Class to steer the boat
class Servo():
    
    #Initialize Servo Object
    def __init__(self, number, kit, isBack):
        self.kit = kit
        self.number = number
        self.isBack = isBack
        
    #Set servo to 0 degrees
    def reset(self):
        self.kit.servo[self.number].angle = 0
        
    #Move to the degree location (0 - 180).
    def move(self, deg):
        if self.isBack:
            self.kit.servo[self.number].angle = 95
        else:
            self.kit.servo[self.number].angle = deg