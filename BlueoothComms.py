import serial



class BluetoothComms:
    
    def __init__(self):
        self.ser = serial.Serial('/dev/rfcomm0', 9600)
        print(self.ser.name)
        self.ser.flushInput()

    def read(self):
        while True:
            lineIn = self.ser.readline()
            lineIn.decode("utf-8")
            lineIn.replace("'", "")
            lineIn.lstrip("b")
            lineIn.rstrip("\r\n")
            print(lineIn)
        
thing = BluetoothComms()
thing.read()