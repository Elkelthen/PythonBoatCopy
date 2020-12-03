import time
from CONTROL import AutomaticMotorControl as AMC
from CONTROL.Servo import Servo
from CONTROL.ESC import ESC
from DAQ.DataAcquisition import AccelerometerCompass, GPS
from simple_pid import PID
from COMMS.BluetoothComms import BluetoothComms as BC
import threading
from adafruit_servokit import ServoKit
import atexit

############################### GLOBAL VARIABLES ######################################

ACC_G = 0
HEADING_G = 0
CURRENT_LAT_G = 10
CURRENT_LONG_G = 10
TARGET_LAT_G = 0
TARGET_LONG_G = 0


############################## END GLOBAL VARIABLES ###################################

################################### FLAGS #############################################

NEW_INFO_F = False

################################ END FLAGS ############################################


class DataThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.AccelCompass = AccelerometerCompass()
        self.GPS = GPS()

    def run(self):
        global NEW_INFO_F, ACC_G, HEADING_G, CURRENT_LAT_G, CURRENT_LONG_G

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
                    print("Lat: %.3fg \t Long: %.3fg" % (self.GPS.getLat(), self.GPS.getLong()))
                if currentLong != CURRENT_LONG_G:
                    CURRENT_LONG_G = currentLong
                    print("Lat: %.3fg \t Long: %.3fg" % (self.GPS.getLat(), self.GPS.getLong()))

                NEW_INFO_F = True

class ControlThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

        # Initialize ServoKit for PWM Hat
        self.kit = ServoKit(channels=16)

        # Initialize Servos
        self.MotorControlX = Servo(2, self.kit, False)
        self.MotorControlX.reset()

        self.MotorControlY = Servo(3, self.kit, False)
        self.MotorControlY.reset()

        self.MotorControlXBack = Servo(4, self.kit, True)
        self.MotorControlXBack.reset()

        self.MotorControlYBack = Servo(5, self.kit, True)
        self.MotorControlYBack.reset()

        # Initialize ESC
        self.ESC = ESC(0, self.kit)
        self.ESC.reset()

        self.ESCBack = ESC(1, self.kit)
        self.ESC.reset()

    def run(self):

        global NEW_INFO_F

        # PID CONTROLLER
        self.pid = PID(1, 0.1, 0.05, setpoint=1)
        self.pid.output_limits = (0, 100)

        while (True):
            if NEW_INFO_F:

                #Front Assembly
                AMC.setThrustDirection(HEADING_G, TARGET_LAT_G, TARGET_LONG_G, CURRENT_LAT_G, CURRENT_LONG_G, self.MotorControlX, self.MotorControlY)
                AMC.setThrustSpeed(TARGET_LAT_G, TARGET_LONG_G, CURRENT_LONG_G, CURRENT_LAT_G, self.ESC)

                #Rear Assembly
                AMC.setThrustDirection(HEADING_G, TARGET_LAT_G, TARGET_LONG_G, CURRENT_LAT_G, CURRENT_LONG_G, self.MotorControlXBack, self.MotorControlYBack)
                AMC.setThrustSpeed(TARGET_LAT_G, TARGET_LONG_G, CURRENT_LONG_G, CURRENT_LAT_G, self.ESCBack)

                NEW_INFO_F = False

class CommsThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        bc = None

    def run(self):

        global TARGET_LAT_G, TARGET_LONG_G

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

#Putting these cleanup methods here because I need to make sure
#The Control ESC will always stop spinning if the program exits.
#The others will probably come in handy at some point.

def cleanUpData():
    pass

def cleanUpControl(ESC):
    ESC.reset()

def cleanUpComms():
    pass

if __name__ == "__main__":

    DAQ = DataThread()
    CTL = ControlThread()
    COM = CommsThread()

    atexit.register(cleanUpData)
    atexit.register(cleanUpComms)
    atexit.register(cleanUpControl, CTL.ESC)

    DAQ.start()
    CTL.start()
    COM.start()

    # Keep the program running. If this isn't here we instantly exit.
    while 1:
        time.sleep(1)