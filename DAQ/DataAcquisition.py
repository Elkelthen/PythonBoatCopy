"""
General sensor data getters
"""

from . import lsm303d
from .grove_gps_data import GPS as g

# Statics because Pylint says this is better

def getAccelX(accelList):
    """
    Get specific X component from a list (requires getAccelAll() first).
    :param accelList:
    :return:
    """
    return accelList[0]


def getAccelY(accelList):
    """
    Get specific Y component from a list (requires getAccelAll() first).
    :param accelList:
    :return:
    """
    return accelList[1]


def getAccelZ(accelList):
    """
    Get specific Z component from a list (requires getAccelAll() first).
    :param accelList:
    :return:
    """
    return accelList[2]


class AccelerometerCompass():
    """
    Getters for the lsm303d Acc/Compass breakout.
    """

    def __init__(self):
        self.accMag = lsm303d.lsm303d()

    def getAccelAll(self):
        """
        Get all Accelerometer Values as a list.
        :return:
        """
        return self.accMag.getRealAccel()

    def getCompassHeading(self):
        """
        get heading
        :return:
        """
        heading = self.accMag.getHeading()
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
        self.gps.getLatLong()

    def getLat(self):
        """
        :return: gps latitude
        """
        return self.gps.lat

    def getLong(self):
        """
        :return: gps longitude
        """
        return self.gps.long
