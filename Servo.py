import RPi.GPIO as GPIO
import time


#Function to change from degrees to pulse width range.
def degreesToPulse(deg):
    #NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
    #This Function converts from one number range to another, provided both ranges are nonzero
    pulse = (((deg - 0) * (12 - 2)) / (180 - 0)) + 2
    return pulse

#Basic Servo Class to steer the boat
class Servo():
    
    #Initialize Servo Object
    def __init__(self, pin, freq):
        self.servo = GPIO.PWM(pin, freq)
        
    #Set servo to 0 degrees
    def reset(self):
        self.servo.start(2.0)
        
    #Move to the degree location (0 - 180).
    def move(self, deg):
        self.servo.ChangeDutyCycle(degreesToPulse(deg))

#SERVOS HAVE A PROBLEM WITH JITTERING AFTER THEY HAVE GONE TO THEIR REQUESTED LOCATION.
#I THINK THAT THREE WRAPS ON A FERRITE CORE WILL SOLVE THIS PROBLEM BUT I'M NOT SURE
#SEEMS LIKE THE UNDERLYING PROBLEM IS "NOISE" ON THE CPU? A CONTROL HAT WOULD ALSO SOLVE
#THIS I THINK BUT I'D RATHER KEEP THE GPIO OPEN FOR OTHER THINGS.