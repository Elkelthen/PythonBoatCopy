"""BluetoothComms.py

Lower level control of the bluetooth communications between phone and raspi.

"""

from bluetooth import BluetoothSocket, RFCOMM, PORT_ANY


class BluetoothComms():
    """
    Initialize Bluetooth Comms
    """

    def __init__(self):

        self.serverSock=BluetoothSocket(RFCOMM)
        self.serverSock.bind(("", PORT_ANY))
        self.serverSock.settimeout(1.0)
        self.serverSock.listen(1)
        self.clientSock, self.clientInfo = self.serverSock.accept()
        self.clientSock.settimeout(1.0)

    def read(self):
        """
        Take input data from phone
        :return:
        """
        try:
            data = self.clientSock.recv(1024).decode('utf-8')
            return data
        except IOError:
            pass

    def write(self, msg):
        """
        Send output data to phone
        :param msg:
        :return:
        """
        try:
            print("sending")
            self.clientSock.send(msg.encode())
        except IOError:
            pass
