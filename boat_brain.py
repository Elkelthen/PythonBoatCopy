"""boat_brain.py

This is the main file for the project. Running this should start the boat.

"""
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
        threading.Thread.__init__(self)
        self.accel_compass = AccelerometerCompass()
        self.gps = GPS()

    def run(self):

        while True:
            acc = self.accel_compass.get_accel_all()
            heading = self.accel_compass.get_compass_heading()
            self.gps.read()
            current_lat = self.gps.get_lat()
            current_long = self.gps.get_long()

            if not data_globals.NEW_INFO_F:
                if acc != data_globals.ACC_G:
                    data_globals.ACC_G = acc
                    print("Acceleration of X,Y,Z is %.3fg, %.3fg, %.3fg" % (acc[0], acc[1], acc[2]))
                if heading != data_globals.HEADING_G:
                    data_globals.HEADING_G = heading
                    print("Heading %.3f degrees\n" % (heading))
                if current_lat != data_globals.CURRENT_LAT_LONG_G[0]:
                    data_globals.CURRENT_LAT_LONG_G[1] = current_lat
                    print("Lat: %.3fg \t Long: %.3fg" % (self.gps.get_lat(), self.gps.get_long()))
                if current_long != data_globals.CURRENT_LAT_LONG_G[1]:
                    data_globals.CURRENT_LAT_LONG_G[0] = current_long
                    print("Lat: %.3fg \t Long: %.3fg" % (self.gps.get_lat(), self.gps.get_long()))

                data_globals.NEW_INFO_F = True


class ControlThread(threading.Thread):
    """
    Initialize Control Thread
    """

    def __init__(self):
        threading.Thread.__init__(self)

        # Initialize ServoKit for PWM Hat
        self.kit = ServoKit(channels=16)

        self.front_thruster = Thruster(self.kit, 0, 2, 3, 111, 79, 97, 71)
        self.back_thruster = Thruster(self.kit, 1, 4, 5, 94, 67, 107, 80)

    def run(self):

        while True:
            if data_globals.NEW_INFO_F:
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

                data_globals.NEW_INFO_F = False


class CommsThread(threading.Thread):
    """
    Initialize Communications Thread
    """

    def __init__(self):
        """
        Set up for the loop
        """
        threading.Thread.__init__(self)
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


def clean_up_control(esc):
    """
    Clean up Control Process at end of program
    :param esc:
    :return:
    """
    esc.reset()


def clean_up_comms():
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
    atexit.register(clean_up_control, CTL.front_thruster.esc)

    DAQ.start()
    CTL.start()
    COM.start()

    # Keep the program running. If this isn't here we instantly exit.
    while 1:
        time.sleep(1)
