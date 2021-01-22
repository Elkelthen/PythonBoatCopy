import serial, time

def readlineCR(ser):
    rv = ""
    while True:
        time.sleep(0.001)  # This is the critical part.  A small pause
        # works really well here.
        ch = ser.read().decode('utf-8')
        rv += ch
        if ch == '\r' or ch == '':
            return rv


class GPS:
    # The GPS module used is a Grove GPS module http://www.seeedstudio.com/depot/Grove-GPS-p-959.html
    inp = []
    # Refer to SIM28 NMEA spec file http://www.seeedstudio.com/wiki/images/a/a0/SIM28_DATA_File.zip
    GGA = []

    def __init__(self):
        self.ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=0)  # Open the serial port at 9600 baud
        self.ser.flush()
        self.lat = -1
        self.long = -1

    # Read data from the GPS
    def read(self):
        while True:
            # GPS.inp=ser.readline()
            GPS.inp = readlineCR(self.ser).strip()
            if GPS.inp[:6] == '$GPGGA':  # GGA data , packet 1, has all the data we need
                break
            time.sleep(0.1)
        try:
            ind = GPS.inp.index('$GPGGA', 5, len(
                GPS.inp))  # Sometimes multiple GPS data packets come into the stream. Take the data only after the last '$GPGGA' is seen
            GPS.inp = GPS.inp[ind:]
        except ValueError:
            print("")
        GPS.GGA = GPS.inp.split(",")  # Split the stream into individual parts
        self.lat = float(GPS.GGA[2])/100
        self.long = float(GPS.GGA[4])/100
        if GPS.GGA[3] == "S":
            self.lat *= -1
        if GPS.GGA[5] == "W":
            self.long *= -1
        return [GPS.GGA]

    # Split the data into individual elements
    def vals(self):
        time = GPS.GGA[1]
        lat = GPS.GGA[2]
        lat_ns = GPS.GGA[3]
        long = GPS.GGA[4]
        long_ew = GPS.GGA[5]
        fix = GPS.GGA[6]
        sats = GPS.GGA[7]
        alt = GPS.GGA[9]
        return [time, fix, sats, alt, lat, lat_ns, long, long_ew]
