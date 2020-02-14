import RPi.GPIO as GPIO
import time
import pigpio
import AutomaticMotorControl as AMC
from Servo import Servo
from ESC import ESC
from DataAcquisition import AccelerometerCompass, GPS
from simple_pid import PID
import numpy

#Set up a servo.
servoX = 12
servoY = 5
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
#AccelCompass = AccelerometerCompass()
GPS = GPS()
    
#PID CONTROLLER
pid = PID(0, 0, 1, setpoint = 1000)
pid.output_limits = (0, 100)
    

for i in numpy.arange(-0.99,-1.00,-0.001):
#while(True):
    try:
        time.sleep(1)
        #DAQ
        #acc = AccelCompass.getAccelAll()
        #heading = AccelCompass.getCompassHeading()
        #OUTPUT TO COMMAND LINE
        #print("Acceleration of X,Y,Z is %.3fg, %.3fg, %.3fg" %(acc[0],acc[1],acc[2]))
        #print("Heading %.3f degrees\n" %(heading))
        #DAQ
        GPS.read()
        currentLat = GPS.getLat()
        currentLong = GPS.getLong()
        print("Lat: %.3fg \t Long: %.3fg" %(GPS.getLat(),GPS.getLong()))
        #OUTPUT TO MOTORS
        #MotorControlX.move(90)
        #AMC.setThrustDirection(heading, 10, 10, currentLat, currentLong, MotorControlX, MotorControlY)
        futureLong = i
        futureLat = i
        AMC.setThrustSpeed(futureLong, futureLat, pid, currentLong, currentLat, ESC)
        #for i in range(0,10):
            
        
    except:
        GPIO.cleanup()
        exit()

