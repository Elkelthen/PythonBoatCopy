"""BoatBrain.py

This is the main file for the project. Running this should start the boat.

"""

import time
import threading
import atexit
from adafruit_servokit import ServoKit
from CONTROL import AutomaticMotorControl as AMC
from CONTROL.Servo import Servo
from CONTROL.ESC import ESC
from DAQ.DataAcquisition import AccelerometerCompass, GPS
from COMMS.BluetoothComms import BluetoothComms as BC



############################### GLOBAL VARIABLES ######################################

ACC_G = 0
HEADING_G = 0

#(Long, Lat) (X, Y)
CURRENT_LAT_LONG_G = [10, 10]
TARGET_LAT_LONG_G = [0, 0]


############################## END GLOBAL VARIABLES ###################################

################################### FLAGS #############################################

NEW_INFO_F = False

################################ END FLAGS ############################################


class DataThread(threading.Thread):
    """
    Initialize Data Thread
    """

    def __init__(self):
        threading.Thread.__init__(self)
        self.accelCompass = AccelerometerCompass()
        self.gps = GPS()

    def run(self):
        global NEW_INFO_F, ACC_G, HEADING_G, CURRENT_LAT_LONG_G

        while True:
            acc = self.accelCompass.getAccelAll()
            heading = self.accelCompass.getCompassHeading()
            self.gps.read()
            currentLat = self.gps.getLat()
            currentLong = self.gps.getLong()

            if not NEW_INFO_F:
                if acc != ACC_G:
                    ACC_G = acc
                    print("Acceleration of X,Y,Z is %.3fg, %.3fg, %.3fg" % (acc[0], acc[1], acc[2]))
                if heading != HEADING_G:
                    HEADING_G = heading
                    print("Heading %.3f degrees\n" % (heading))
                if currentLat != CURRENT_LAT_LONG_G[0]:
                    CURRENT_LAT_LONG_G[1] = currentLat
                    print("Lat: %.3fg \t Long: %.3fg" % (self.gps.getLat(), self.gps.getLong()))
                if currentLong != CURRENT_LAT_LONG_G[1]:
                    CURRENT_LAT_LONG_G[0] = currentLong
                    print("Lat: %.3fg \t Long: %.3fg" % (self.gps.getLat(), self.gps.getLong()))

                NEW_INFO_F = True

class ControlThread(threading.Thread):
    """
    Initialize Control Thread
    """

    def __init__(self):
        threading.Thread.__init__(self)

        # Initialize ServoKit for PWM Hat
        self.kit = ServoKit(channels=16)

        # Initialize Servos
        self.motorControlX = Servo(2, self.kit, False)
        self.motorControlX.reset()

        self.motorControlY = Servo(3, self.kit, False)
        self.motorControlY.reset()

        self.motorControlXBack = Servo(4, self.kit, True)
        self.motorControlXBack.reset()

        self.motorControlYBack = Servo(5, self.kit, True)
        self.motorControlYBack.reset()

        # Initialize ESC
        self.esc = ESC(0, self.kit)
        self.esc.reset()

        self.escBack = ESC(1, self.kit)
        self.esc.reset()

    def run(self):

        global NEW_INFO_F, TARGET_LAT_LONG_G

        while True:
            if NEW_INFO_F:

                #Front Assembly
                AMC.setThrustDirection(HEADING_G, TARGET_LAT_LONG_G, CURRENT_LAT_LONG_G,
                                       self.motorControlX, self.motorControlY)
                AMC.setThrustSpeed(TARGET_LAT_LONG_G, CURRENT_LAT_LONG_G, self.esc)


                #Rear Assembly
                AMC.setThrustDirection(HEADING_G, TARGET_LAT_LONG_G, CURRENT_LAT_LONG_G,
                                       self.motorControlXBack, self.motorControlYBack)
                AMC.setThrustSpeed(TARGET_LAT_LONG_G, CURRENT_LAT_LONG_G, self.escBack)

                NEW_INFO_F = False

class CommsThread(threading.Thread):
    """
    Initialize Communications Thread
    """

    def __init__(self):
        threading.Thread.__init__(self)
        self.bluetoothComm = None

    def run(self):

        global TARGET_LAT_LONG_G

        while True:
            try:
                # Bluetooth Serial Comms
                if self.bluetoothComm is None:
                    self.bluetoothComm = BC()
            except Exception as error:
                print(str(error))
                print("No device")

            try:
                time.sleep(1)
                print("\n\n\n\n\n")
                # Read input from Bluetooth Comms
                try:
                    print("Trying")
                    read = self.bluetoothComm.read().split(" ")
                    if read is None:
                        pass
                    elif 'S' in read[0]:
                        # ESC.setSpeed(int(read[0].replace('S', '')))
                        # TODO: MANUAL SPEED CONTROL ACROSS THREADS
                        pass
                    elif 'GET' in read[0]:
                        sendStream = 'Heading:' + str(HEADING_G) +\
                                     ' GoX:' + str(TARGET_LAT_LONG_G[1]) +\
                                     ' GoY:' + str(TARGET_LAT_LONG_G[0]) +\
                                     ' Lat:' + str(CURRENT_LAT_LONG_G[0]) +\
                                     ' Long:' + str(CURRENT_LAT_LONG_G[1])
                        self.bluetoothComm.write(sendStream)
                    else:
                        print(read)
                        TARGET_LAT_LONG_G[1] = int(read[0])
                        TARGET_LAT_LONG_G[0] = int(read[1])
                        print(TARGET_LAT_LONG_G[1])
                        print(TARGET_LAT_LONG_G[0])
                except:
                    print("No (new) values from bluetooth")
            except:
                pass

#Putting these cleanup methods here because I need to make sure
#The Control ESC will always stop spinning if the program exits.
#The others will probably come in handy at some point.

def cleanUpData():
    """
    Clean up data process at end of program.
    :return:
    """


def cleanUpControl(esc):
    """
    Clean up Control Process at end of program
    :param esc:
    :return:
    """
    esc.reset()

def cleanUpComms():
    """
    Clean up communications at end of program.
    :return:
    """


if __name__ == "__main__":

    DAQ = DataThread()
    CTL = ControlThread()
    COM = CommsThread()

    atexit.register(cleanUpData)
    atexit.register(cleanUpComms)
    atexit.register(cleanUpControl, CTL.esc)

    DAQ.start()
    CTL.start()
    COM.start()

    # Keep the program running. If this isn't here we instantly exit.
    while 1:
        time.sleep(1)
