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
import threading
from adafruit_servokit import ServoKit


############################### GLOBAL VARIABLES ######################################

ACC_G = 0
HEADING_G = 0
CURRENT_LAT_G = 0
CURRENT_LONG_G = 0
TARGET_LAT_G = 0
TARGET_LONG_G = 0


############################## END GLOBAL VARIABLES ###################################

################################### FLAGS #############################################

NEW_INFO_F = False

################################ END FLAGS ############################################


class DataThread(threading.Thread):
    global NEW_INFO_F, ACC_G, HEADING_G, CURRENT_LAT_G, CURRENT_LONG_G
    
    def __init__(self):
        self.AccelCompass = AccelerometerCompass()
        self.GPS = GPS()

    def run(self):
        while True:
            acc = self.AccelCompass.getAccelAll()
            heading = self.AccelCompass.getCompassHeading()
            self.GPS.read()
            currentLat = self.GPS.getLat()
            currentLong = self.GPS.getLong()

            if NEW_INFO_F == False:
                if acc != ACC_G:
                    ACC_G = acc
                    print("Acceleration of X,Y,Z is %.3fg, %.3fg, %.3fg" % (acc[0], acc[1], acc[2]))
                if heading != HEADING_G:
                    HEADING_G = heading
                    print("Heading %.3f degrees\n" % (heading))
                if currentLat != CURRENT_LAT_G:
                    CURRENT_LAT_G = currentLat
                    print("Lat: %.3fg \t Long: %.3fg" % (GPS.getLat(), GPS.getLong()))
                if currentLong != CURRENT_LONG_G:
                    CURRENT_LONG_G = currentLong
                    print("Lat: %.3fg \t Long: %.3fg" % (GPS.getLat(), GPS.getLong()))

                NEW_INFO_F = True

class ControlThread(threading.Thread):

    def __init__(self):
        # Set up a servo.
        global NEW_INFO_F

        # Initialize ServoKit for PWM Hat
        self.kit = ServoKit(channels=16)

        # Initialize Servos
        self.MotorControlX = Servo(2, kit)
        self.MotorControlX.reset()

        self.MotorControlY = Servo(3, kit)
        self.MotorControlY.reset()

        # Initialize ESC
        self.ESC = ESC(4, kit)
        self.ESC.reset()

        # PID CONTROLLER
        self.pid = PID(10, 0, 75, setpoint=0)
        self.pid.output_limits = (0, 100)

    def run(self):
        while (True):
            if NEW_INFO_F:
                AMC.setThrustDirection(HEADING_G, TARGET_LAT_G, TARGET_LONG_G, CURRENT_LAT_G, CURRENT_LONG_G, self.MotorControlX, self.MotorControlY)
                AMC.setThrustSpeed(TARGET_LAT_G, TARGET_LONG_G, self.pid, CURRENT_LONG_G, CURRENT_LAT_G, self.ESC)
                NEW_INFO_F = False

class CommsThread(threading.Thread):
    global TARGET_LAT_G, TARGET_LONG_G

    def __init__(self):
        bc = None

    def run(self):
        while True:
            try:
                # Bluetooth Serial Comms
                if bc == None:
                    bc = BC()
            except Exception as e:
                print(str(e))
                print("No device")

            try:
                time.sleep(1)
                print("\n\n\n\n\n")
                # Read input from Bluetooth Comms
                try:
                    print("Trying")
                    read = bc.read().split(" ")
                    if read is None:
                        pass
                    elif 'S' in read[0]:
                        ESC.setSpeed(int(read[0].replace('S', '')))
                    elif 'GET' in read[0]:
                        sendStream = 'Heading:' + str(HEADING_G) + ' GoX:' + str(TARGET_LAT_G) + ' GoY:' + str(
                            TARGET_LONG_G) + ' Lat:' + str(CURRENT_LAT_G) + ' Long:' + str(CURRENT_LONG_G)
                        bc.write(sendStream)
                    else:
                        print(read)
                        TARGET_LAT_G = int(read[0])
                        TARGET_LONG_G = int(read[1])
                        print(TARGET_LAT_G)
                        print(TARGET_LONG_G)
                except Exception as e:
                    print("No (new) values from bluetooth")
            except:
                pass

if __name__ == "__main__":

    DAQ = threading.Thread(target=DataThread)
    CTL = threading.Thread(target=ControlThread)
    COM = threading.Thread(target=CommsThread)

    while 1:
        time.sleep(1)
        print(str(HEADING_G))


