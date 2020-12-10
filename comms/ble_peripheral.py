"""
BLE beaconing class, uses data_characteristic.py for the actual information of the class.
"""

from pybleno import Bleno, BlenoPrimaryService
from .data_characteristic import DataCharacteristic


class BLEPeripheral:
    """
    Sets up the raspi to act as a BLE beacon.
    """

    def __init__(self):
        self.bleno = Bleno()
        self.bleno.on('stateChange', self.on_state_change)
        self.bleno.on('advertisingStart', self.on_advertising_start)
        self.bleno.start()

    def on_state_change(self, state):
        """
        :param state On or Off:
        :return:
        """
        print('on -> stateChange: ' + state)
        if state == 'poweredOn':
            self.bleno.startAdvertising('echo', ['ec00'])
        else:
            self.bleno.stopAdvertising()

    def on_advertising_start(self, error):
        """
        :param error:
        :return:
        """
        print('on -> advertisingStart: ' + ('error ' + error if error else 'success'))
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
        quit advertising
        :return:
        """
        self.bleno.stopAdvertising()
        self.bleno.disconnect()
