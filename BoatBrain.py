import RPi.GPIO as GPIO
import time
import pigpio
import AutomaticMotorControl as AMC
from Servo import Servo
from ESC import ESC
from DataAcquisition import AccelerometerCompass, GPS
from simple_pid import PID
from BluetoothComms import BluetoothComms as BC
import numpy



#Set up a servo.
servoX = 17
servoY = 27
GPIO.setmode(GPIO.BCM)
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
pid = PID(10, 0, 75, setpoint = 0)
pid.output_limits = (0, 100)
    

xCoord = 10
yCoord = 10

bc = None

while(True):
    try:
        #Bluetooth Serial Comms
        if bc == None:
            bc = BC()
    except Exception as e:
        print(str(e))
        print("No device")
    
    try:
        time.sleep(1)
        print("\n\n\n\n\n")
        #Read input from Bluetooth Comms
        try:
            print("Trying")
            read = bc.read().split(" ")
            if read == None:
                pass
            elif 'S' in read[0]:
                ESC.setSpeed(int(read[0].replace('S','')))
            elif 'GET' in read[0]:
                sendStream = 'Heading:' + str(heading) + ' GoX:' + str(xCoord) + ' GoY:' + str(yCoord) + ' Lat:' + str(currentLat) + ' Long:' + str(currentLong)
                bc.write(sendStream)
            else:
                print(read)
                xCoord = int(read[0])
                yCoord = int(read[1])
                print(xCoord)
                print(yCoord)
        except Exception as e:
            print("No (new) values from bluetooth")

        #DAQ
        acc = AccelCompass.getAccelAll()
        heading = AccelCompass.getCompassHeading()
        #OUTPUT TO COMMAND LINE
        print("Acceleration of X,Y,Z is %.3fg, %.3fg, %.3fg" %(acc[0],acc[1],acc[2]))
        print("Heading %.3f degrees\n" %(heading))
        #DAQ
        GPS.read()
        currentLat = GPS.getLat()
        currentLong = GPS.getLong()
        print("Lat: %.3fg \t Long: %.3fg" %(GPS.getLat(),GPS.getLong()))
        #OUTPUT TO MOTORS
        #MotorControlX.move(90)
        AMC.setThrustDirection(heading, xCoord, yCoord, currentLat, currentLong, MotorControlX, MotorControlY)
        AMC.setThrustSpeed(xCoord, yCoord, pid, currentLong, currentLat, ESC)
        
    except:
        GPIO.cleanup()
        exit()
