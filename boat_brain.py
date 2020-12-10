"""boat_brain.py

This is the main file for the project. Running this should start the boat.

"""

import time
import threading
import atexit
from adafruit_servokit import ServoKit
from control import automatic_motor_control as AMC
from control.servo import Servo
from control.esc import ESC
from daq.data_acquisition import AccelerometerCompass, GPS
from comms.bluetooth_comms import BluetoothComms as BC
from comms.ble_peripheral import BLEPeripheral

############################### GLOBAL VARIABLES ######################################

ACC_G = 0
HEADING_G = 0

# (Long, Lat) (X, Y)
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
        self.accel_compass = AccelerometerCompass()
        self.gps = GPS()

    def run(self):
        global NEW_INFO_F, ACC_G, HEADING_G, CURRENT_LAT_LONG_G

        while True:
            acc = self.accel_compass.get_accel_all()
            heading = self.accel_compass.get_compass_heading()
            self.gps.read()
            current_lat = self.gps.get_lat()
            current_long = self.gps.get_long()

            if not NEW_INFO_F:
                if acc != ACC_G:
                    ACC_G = acc
                    print("Acceleration of X,Y,Z is %.3fg, %.3fg, %.3fg" % (acc[0], acc[1], acc[2]))
                if heading != HEADING_G:
                    HEADING_G = heading
                    print("Heading %.3f degrees\n" % (heading))
                if current_lat != CURRENT_LAT_LONG_G[0]:
                    CURRENT_LAT_LONG_G[1] = current_lat
                    print("Lat: %.3fg \t Long: %.3fg" % (self.gps.get_lat(), self.gps.get_long()))
                if current_long != CURRENT_LAT_LONG_G[1]:
                    CURRENT_LAT_LONG_G[0] = current_long
                    print("Lat: %.3fg \t Long: %.3fg" % (self.gps.get_lat(), self.gps.get_long()))

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
        self.motor_control_x = Servo(2, self.kit, False)
        self.motor_control_x.reset()

        self.motor_control_y = Servo(3, self.kit, False)
        self.motor_control_y.reset()

        self.motor_control_x_back = Servo(4, self.kit, True)
        self.motor_control_x_back.reset()

        self.motor_control_y_back = Servo(5, self.kit, True)
        self.motor_control_y_back.reset()

        # Initialize ESC
        self.esc = ESC(0, self.kit)
        self.esc.reset()

        self.esc_back = ESC(1, self.kit)
        self.esc_back.reset()

    def run(self):

        global NEW_INFO_F, TARGET_LAT_LONG_G

        while True:
            if NEW_INFO_F:
                # Front Assembly
                AMC.set_thrust_direction(HEADING_G, TARGET_LAT_LONG_G, CURRENT_LAT_LONG_G,
                                         self.motor_control_x, self.motor_control_y)
                AMC.set_thrust_speed(TARGET_LAT_LONG_G, CURRENT_LAT_LONG_G, self.esc)

                # Rear Assembly
                AMC.set_thrust_direction(HEADING_G, TARGET_LAT_LONG_G, CURRENT_LAT_LONG_G,
                                         self.motor_control_x_back, self.motor_control_y_back)
                AMC.set_thrust_speed(TARGET_LAT_LONG_G, CURRENT_LAT_LONG_G, self.esc_back)

                NEW_INFO_F = False


class CommsThread(threading.Thread):
    """
    Initialize Communications Thread
    """

    def __init__(self):
        threading.Thread.__init__(self)
        self.bluetooth_comm = None

    def run(self):

        global TARGET_LAT_LONG_G

        # Adding this to remember where it goes later.
        ble_periph = BLEPeripheral()

        while True:
            try:
                # Bluetooth Serial Comms
                if self.bluetooth_comm is None:
                    self.bluetooth_comm = BC()
            except Exception as error:
                print(str(error))
                print("No device")

            try:
                time.sleep(1)
                print("\n\n\n\n\n")
                # Read input from Bluetooth Comms
                try:
                    print("Trying")
                    read = self.bluetooth_comm.read().split(" ")
                    if read is None:
                        pass
                    elif 'S' in read[0]:
                        # ESC.setSpeed(int(read[0].replace('S', '')))
                        # TODO: MANUAL SPEED CONTROL ACROSS THREADS
                        pass
                    elif 'GET' in read[0]:
                        send_stream = 'Heading:' + str(HEADING_G) + \
                                      ' GoX:' + str(TARGET_LAT_LONG_G[1]) + \
                                      ' GoY:' + str(TARGET_LAT_LONG_G[0]) + \
                                      ' Lat:' + str(CURRENT_LAT_LONG_G[0]) + \
                                      ' Long:' + str(CURRENT_LAT_LONG_G[1])
                        self.bluetooth_comm.write(send_stream)
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


# Putting these cleanup methods here because I need to make sure
# The Control ESC will always stop spinning if the program exits.
# The others will probably come in handy at some point.

def clean_up_data():
    """
    Clean up data process at end of program.
    :return:
    """


def clean_up_control(esc):
    """
    Clean up Control Process at end of program
    :param esc:
    :return:
    """
    esc.reset()


def clean_up_comms(BLE):
    BLE.clean_up()
    """
    Clean up communications at end of program.
    :return:
    """


if __name__ == "__main__":

    DAQ = DataThread()
    CTL = ControlThread()
    COM = CommsThread()

    atexit.register(clean_up_data)
    atexit.register(clean_up_comms)
    atexit.register(clean_up_control, CTL.esc)

    DAQ.start()
    CTL.start()
    COM.start()

    # Keep the program running. If this isn't here we instantly exit.
    while 1:
        time.sleep(1)
