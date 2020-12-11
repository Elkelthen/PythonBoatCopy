"""
Adafruit's implementation of BLE two way communication.
"""
from adafruit_ble_radio import Radio


class BLERadio:
    """
    Class structure for availability to the rest of the program.
    """

    def __init__(self):
        """
        set up
        """
        self.radio = Radio(channel = 0)

    def send(self, msg):
        """
        :param msg:
        :return: None
        """
        self.radio.send(msg)

    def rcv(self):
        """
        Currently using receive_full because it gives more info, but could
        use receive() for a string of the message only.
        :return looks like a list [message, message strength, timestamp]:
        """
        return self.radio.receive_full()
