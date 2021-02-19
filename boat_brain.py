"""boat_brain.py

This is the main file for the project. Running this should start the boat.

"""
import os
import random
import time
import threading
import atexit
from adafruit_servokit import ServoKit
import data_globals
from control import automatic_motor_control as AMC
from control.thruster_module import Thruster
from daq.data_acquisition import AccelerometerCompass, GPS
from comms.ble_central import Central
from comms.ble_peripheral import BLEPeripheral


class DataThread(threading.Thread):
    """
    Initialize Data Thread
    """

    def __init__(self):
        threading.Thread.__init__(self, daemon=True)
        self.accel_compass = AccelerometerCompass()

    def run(self):
        i = 0
        while True:
            data_globals.ACC_G = self.accel_compass.get_accel_all()
            data_globals.HEADING_G = self.accel_compass.get_compass_heading()
            time.sleep(0.01)


class GPSThread(threading.Thread):
    """
    Initialize GPS Thread.
    This is necessary because the GPS takes a LONG time to read
    relative to the other sensors, but we can't have it block the
    rest of the program or responsiveness goes way down, so it gets
    its own thread. Lucky Duck.
    """

    def __init__(self):
        """
        Initialize GPS objects.
        """
        threading.Thread.__init__(self, daemon=True)
        self.gps = GPS()

    def run(self):
        while True:
            self.gps.read()
            data_globals.CURRENT_LAT_LONG_G[0] = self.gps.get_lat()
            data_globals.CURRENT_LAT_LONG_G[1] = self.gps.get_long()
            time.sleep(1)


class ControlThread(threading.Thread):
    """
    Initialize Control Thread
    """

    def __init__(self):
        threading.Thread.__init__(self, daemon=True)

        # Initialize ServoKit for PWM Hat
        self.kit = ServoKit(channels=16)

        self.front_thruster = Thruster(self.kit, 0, 2, 3, 142, 112, 100, 70)
        self.back_thruster = Thruster(self.kit, 1, 4, 5, 100, 70, 112, 82)

    def run(self):

        while True:
            # Front Assembly
            AMC.set_thrust_direction(data_globals.HEADING_G, data_globals.TARGET_LAT_LONG_G,
                                     data_globals.CURRENT_LAT_LONG_G,
                                     self.front_thruster.motor_control_x,
                                     self.front_thruster.motor_control_y)
            AMC.set_thrust_speed(data_globals.TARGET_LAT_LONG_G,
                                 data_globals.CURRENT_LAT_LONG_G,
                                 self.front_thruster.esc)

            # Rear Assembly
            AMC.set_thrust_direction(data_globals.HEADING_G, data_globals.TARGET_LAT_LONG_G,
                                     data_globals.CURRENT_LAT_LONG_G,
                                     self.back_thruster.motor_control_x,
                                     self.back_thruster.motor_control_y)
            AMC.set_thrust_speed(data_globals.TARGET_LAT_LONG_G,
                                 data_globals.CURRENT_LAT_LONG_G,
                                 self.back_thruster.esc)

            time.sleep(0.1)


class CommsThread(threading.Thread):
    """
    Initialize Communications Thread
    """

    def __init__(self):
        """
        Set up for the loop
        """
        threading.Thread.__init__(self,daemon=True)
        self.ble_comm_in = Central()
        self.ble_comm_out = BLEPeripheral()

    def run(self):
        """
        Advertising and Scanning both block, so I've put in a random delay in the advertising
        (between 1 and 3 seconds) so that there is a higher chance that one boat is advertising
        while the other is scanning, and they can actually pass their information along.
        It seems to work very well, from my testing.
        """
        while True:
            # send
            try:
                self.ble_comm_out.turn_on()
                time.sleep(random.randint(1, 3))
            except BlockingIOError:
                print("IO BLOCK")

            # receive
            self.ble_comm_out.turn_off()

            self.ble_comm_in.scan_for_devices(1)
            if self.ble_comm_in.connection_list is not None:
                self.ble_comm_in.get_scan_info()
            else:
                print("Found 0 Devices.")


# Putting these cleanup methods here because I need to make sure
# The Control ESC will always stop spinning if the program exits.
# The others will probably come in handy at some point.

def clean_up_data():
    """
    Clean up data process at end of program.
    :return:
    """


def clean_up_control(esc, esc1):
    """
    Clean up Control Process at end of program
    :param esc:
    :return:
    """
    esc.stop()
    esc1.stop()


def clean_up_comms():
    """
    Clean up communications at end of program.
    :return:
    """


if __name__ == "__main__":

    DAQ = DataThread()
    CTL = ControlThread()
    COM = CommsThread()
    GPS = GPSThread()

    atexit.register(clean_up_data)
    atexit.register(clean_up_comms)
    atexit.register(clean_up_control, CTL.front_thruster.esc, CTL.back_thruster.esc)

    DAQ.start()
    CTL.start()
    COM.start()
    GPS.start()

    data_globals.HOME_G = data_globals.CURRENT_LAT_LONG_G
    print('Starting home is:' data_globals.HOME_G)

    # Keep the program running. If this isn't here we instantly exit.
    while not data_globals.SHUTDOWN_F:
        os.system("clear")
        if data_globals.SET_HOME_F:
            data_globals.HOME_G = data_globals.CURRENT_LAT_LONG_G
            print('Home is now:' data_globals.HOME_G)
        if data_globals.GO_HOME_F:
            data_globals.TARGET_LAT_LONG_G = data_globals.HOME_G
            print('We are going home')
        print("HEADING: ", data_globals.HEADING_G)
        print("THEADING: ", data_globals.TARGET_HEADING_G)
        print("TLONG: ", data_globals.TARGET_LAT_LONG_G[0])
        print("TLAT: ", data_globals.TARGET_LAT_LONG_G[1])
        print("CLONG: ", data_globals.CURRENT_LAT_LONG_G[0])
        print("CLAT: ", data_globals.CURRENT_LAT_LONG_G[1])
        print("ACC: ", data_globals.ACC_G)
        print("ANGLES: ", data_globals.SERVO_ANGLES_G)
        #print("HEADINGS_FILTERED: ", data_globals.HEADING_FILTERED_G)
        time.sleep(1)


