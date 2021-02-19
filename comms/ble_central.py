"""
BLE Central Class (Scanner)
"""
import math
import gc
from bluepy.btle import Scanner, DefaultDelegate, BTLEManagementError
import data_globals


def get_distance_from_rssi(rssi):
    """
    Perform a calc to get the distance based on strength of BLE signal.
    TODO: This doesn't work right, currently.
    :param rssi:
    :return:
    """
    return math.pow(10.0, (((-59) - rssi) / 20))


class Central:
    """
    This class acts as the BLE central functionality, which
    allows us to read other BLE device advertisements.

    If you're looking to send out advertisements of your own,
    look in the ble_peripheral class.
    """

    def __init__(self):
        """
        Initialize class fields.
        """
        self.connection_list = []
        self.peripheral_list = []
        self.scanner = Scanner().withDelegate(ScanDelegate())

    def scan_for_devices(self, timeout):
        """
        Update the connections list
        :param timeout: caller provided. Should be short.
        :return: None
        """
        try:
            self.connection_list = self.scanner.scan(timeout)
        except OSError:
            gc.collect()
            print("Too many files open, bruh :/")
        except BTLEManagementError:
            gc.collect()
            print("Management Error, Passing")


    def get_scan_info(self):
        """
        Handle the information given by devices scanned.
        Probably needs to return the information to the brain,
        to do actual handling in the control portion.
        :return: None (currently)
        """
        for dev in self.connection_list:
            for (adtype, desc, value) in dev.getScanData():
                if "boat_data" in value:
                    print(" %s = %s" % (desc, value))
                    print(dev.rssi)
                    print(get_distance_from_rssi(dev.rssi), "Meters")

                # Below is for a tagalong boat setup.
                # boat_controller is a phone
                # boat_main is reading from phone
                # boat_tag is reading from boat_main
                # Nothing should react to a boat_tag broadcast.

                if "boat_controller" in value:
                    # This should be set to receive the correct values from a phone.
                    print("Setting course")
                    value = value.split()
                    data_globals.TARGET_LAT_LONG_G[1] = float(value[1])
                    data_globals.TARGET_LAT_LONG_G[0] = float(value[2])

                if "boat_main" in value:
                    # This should be set to receive the correct values from boat_main.
                    print("Setting course")
                    data_globals.TARGET_LAT_LONG_G[1] = 10
                    data_globals.TARGET_LAT_LONG_G[0] = 10

                if "shutdown" in value:
                    data_globals.SHUTDOWN_F = True
                if "set_home" in value:
                    data_globals.SET_HOME_F = True
                if "go_home" in value:
                    data_globals.GO_HOME_F = True



class ScanDelegate(DefaultDelegate):
    """
    This came from some test code I was using originally.
    Ideally, this should be refactored into the Central() class,
    right now, this is used by scan_for_devices().
    """

    def __init__(self):
        """
        basic init.
        """
        DefaultDelegate.__init__(self)

    def handle_discovery(self, dev, is_new_dev, is_new_data):
        """
        When a new connection is found (NOT CONNECTED TO), this triggers.
        :param dev:
        :param is_new_dev:
        :param is_new_data:
        :return:
        """
        if is_new_dev:
            print("Discovered ", dev.addr)
        elif is_new_data:
            print("New Data From ", dev.addr)
