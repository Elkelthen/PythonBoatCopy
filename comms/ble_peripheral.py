"""
BLE beaconing class, uses data_characteristic.py for the actual information of the class.
"""

import data_globals
from pybleno import Bleno, BlenoPrimaryService
from .data_characteristic import DataCharacteristic


class BLEPeripheral:
    """
    Sets up the raspi to act as a BLE beacon.
    """

    def __init__(self):
        """
        Basic initializations and bindings.
        """
        self.bleno = Bleno()
        self.bleno.on('advertisingStart', self.on_advertising_start)
        self.bleno.start()

    def turn_on(self):
        """
        Begin advertising
        """
        self.bleno.state = "poweredOn"
        ad_string = "boat_data " + \
                    str(data_globals.CURRENT_LAT_LONG_G[0]) + \
                    str(data_globals.CURRENT_LAT_LONG_G[1])
        self.bleno.startAdvertising(ad_string, ['ec00'])

    def turn_off(self):
        """
        End advertising.
        """
        self.bleno.state = "poweredOff"
        self.bleno.stopAdvertising()

    def on_advertising_start(self, error):
        """
        This binding is necessary for the library or I wouldn't keep it.
        The whole bindings system is a serious PITA.
        """
        if not error:
            self.bleno.setServices([
                BlenoPrimaryService({
                    'uuid': 'ec00',
                    'characteristics': [
                        DataCharacteristic('ec0F')
                    ]
                })
            ])

    def clean_up(self):
        """
        quit
        """
        self.bleno.stopAdvertising()
        self.bleno.disconnect()
