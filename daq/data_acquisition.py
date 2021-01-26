"""
General sensor data getters
"""

from . import lsm303d
from .grove_gps_data import GPS as g
from lsm9ds1_rjg.lsm9ds1 import Driver as lsm9ds1
from lsm9ds1_rjg import I2CTransport


# Statics because Pylint says this is better

def get_accel_x(accel_list):
    """
    Get specific X component from a list (requires getAccelAll() first).
    :param accel_list:
    :return:
    """
    return accel_list[0]


def get_accel_y(accel_list):
    """
    Get specific Y component from a list (requires getAccelAll() first).
    :param accel_list:
    :return:
    """
    return accel_list[1]


def get_accel_z(accel_list):
    """
    Get specific Z component from a list (requires getAccelAll() first).
    :param accel_list:
    :return:
    """
    return accel_list[2]


class AccelerometerCompass():
    """
    Getters for the lsm303d Acc/Compass breakout.
    """

    def __init__(self):
        self.acc_mag = lsm303d.LSM303D()
        # self.acc_mag = lsm9ds1(I2CTransport(1, I2CTransport.I2C_AG_ADDRESS),
        #                        I2CTransport(1, I2CTransport.I2C_MAG_ADDRESS))
        # self.acc_mag.configure()

    def get_accel_all(self):
        """
        Get all Accelerometer Values as a list.
        :return:
        """
        return self.acc_mag.get_real_accel()

    def get_compass_heading(self):
        """
        get heading
        :return:
        """
        heading = self.acc_mag.get_heading()
        return heading


class GPS():
    """
    Initialize GPS Class
    """

    def __init__(self):
        self.gps = g()

    def read(self):
        """
        :return: lat and long values from GPS chip
        """
        try:
            self.gps.read()  # Read from GPS
        except IndexError:
            print("Unable to read")
        except:
            print("String Empty")

    def get_lat(self):
        """
        :return: gps latitude
        """
        return self.gps.lat

    def get_long(self):
        """
        :return: gps longitude
        """
        return self.gps.long
