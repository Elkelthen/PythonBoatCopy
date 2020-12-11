"""boat_brain.py

This is the main file for the project. Running this should start the boat.

"""

import time
import threading
import atexit
import data_globals
from adafruit_servokit import ServoKit
from control import automatic_motor_control as AMC
from control.servo import Servo
from control.esc import ESC
from daq.data_acquisition import AccelerometerCompass, GPS
from comms.ble_radio import BLERadio


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

        while True:
            if data_globals.NEW_INFO_F:
                # Front Assembly
                AMC.set_thrust_direction(data_globals.HEADING_G, data_globals.TARGET_LAT_LONG_G, data_globals.CURRENT_LAT_LONG_G,
                                         self.motor_control_x, self.motor_control_y)
                AMC.set_thrust_speed(data_globals.TARGET_LAT_LONG_G, data_globals.CURRENT_LAT_LONG_G, self.esc)

                # Rear Assembly
                AMC.set_thrust_direction(data_globals.HEADING_G, data_globals.TARGET_LAT_LONG_G, data_globals.CURRENT_LAT_LONG_G,
                                         self.motor_control_x_back, self.motor_control_y_back)
                AMC.set_thrust_speed(data_globals.TARGET_LAT_LONG_G, data_globals.CURRENT_LAT_LONG_G, self.esc_back)

                NEW_INFO_F = False


class CommsThread(threading.Thread):
    """
    Initialize Communications Thread
    """

    def __init__(self):
        threading.Thread.__init__(self)
        self.ble_comm = BLERadio()

    def run(self):
        while True:
            if data_globals.NEW_INFO_F:

                # send
                send_str = str(data_globals.CURRENT_LAT_LONG_G[0]) + " " + str(data_globals.CURRENT_LAT_LONG_G[1])
                self.ble_comm.send(send_str)

                # receive
                from_others = self.ble_comm.rcv()
                if from_others is not None:
                    print(str(from_others))

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
    atexit.register(clean_up_control, CTL.esc)

    DAQ.start()
    CTL.start()
    COM.start()

    # Keep the program running. If this isn't here we instantly exit.
    while 1:
        time.sleep(1)
