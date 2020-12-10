"""
Characteristic for beaconing data about the boat.
"""
import array
from pybleno import Characteristic


class DataCharacteristic(Characteristic):
    """
    initialize the actual characteristic.
    """

    def __init__(self, uuid):
        Characteristic.__init__(self, {
            'uuid': uuid,
            'properties': ['read', 'notify'],
            'value': None
        })

        self._value = array.array('B', [0] * 0)
        self._update_value_callback = None

    def onReadRequest(self, offset, callback):
        print('EchoCharacteristic - %s - onReadRequest: value = %s' %
              (self['uuid'], [hex(c) for c in self._value]))
        callback(Characteristic.RESULT_SUCCESS, self._value[offset:])

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        self._value = data

        print('EchoCharacteristic - %s - onWriteRequest: value = %s' %
              (self['uuid'], [hex(c) for c in self._value]))

        if self._update_value_callback:
            print('EchoCharacteristic - onWriteRequest: notifying')

            self._update_value_callback(self._value)

        callback(Characteristic.RESULT_SUCCESS)

    def onSubscribe(self, maxValueSize, updateValueCallback):
        print('EchoCharacteristic - onSubscribe')

        self._update_value_callback = updateValueCallback

    def onUnsubscribe(self):
        print('EchoCharacteristic - onUnsubscribe')

        self._update_value_callback = None
