import RPi.GPIO as GPIO
import time
import pigpio
import AutomaticMotorControl as AMC
from Servo import Servo
from ESC import ESC
from DataAcquisition import AccelerometerCompass, GPS
from simple_pid import PID

#Set up a servo.
servoX = 12
servoY = 13
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servoX,GPIO.OUT)
GPIO.setup(servoY,GPIO.OUT)
pi = pigpio.pi()

#Initialize Servos
MotorControlX = Servo(servoX, 50)
MotorControlX.reset()

MotorControlY = Servo(servoY, 50)
MotorControlY.reset()

#Initialize ESC
ESC = ESC(4,pi)
ESC.reset()

#Initialize Accel/Compass and GPS
AccelCompass = AccelerometerCompass()
GPS = GPS()
    
#PID CONTROLLER
pid = PID(1, 0.1, 0.05, setpoint = 1)
pid.output_limits = (0, 50)
    

while(True):
    time.sleep(.5)
    #DAQ
    #acc = AccelCompass.getAccelAll()
    heading = AccelCompass.getCompassHeading()
    #OUTPUT TO COMMAND LINE
    #print("Acceleration of X,Y,Z is %.3fg, %.3fg, %.3fg" %(acc[0],acc[1],acc[2]))
    print("Heading %.3f degrees\n" %(heading))
    #DAQ
    GPS.read()
    currentLat = GPS.getLat()
    currentLong = GPS.getLong()
    print("Lat: %.3fg \t Long: %.3fg" %(GPS.getLat(),GPS.getLong()))
    #OUTPUT TO MOTORS
    #MotorControlX.move(90)
    AMC.setThrustDirection(heading, 10, 10, currentLat, currentLong, MotorControlX, MotorControlY)
    #AMC.setThrustSpeed(10, 10, pid, currentLong, currentLat, ESC)

