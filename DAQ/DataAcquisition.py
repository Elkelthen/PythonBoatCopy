from . import lsm303d
from .grove_gps_data import GPS as g

class AccelerometerCompass():
    
    def __init__(self):
        self.acc_mag = lsm303d.lsm303d()
    
    #Get all Accelerometer Values as a list.
    def getAccelAll(self):
        return self.acc_mag.getRealAccel()
    
    #Get specific X Y or Z components from a list (requires getAccelAll() first).
    def getAccelX(self, accelList):
        return accelList[0]
    
    def getAccelY(self, accelList):
        return accelList[1]
    
    def getAccelZ(self, accelList):
        return accelList[2]
    
    #get heading
    def getCompassHeading(self):
        heading = self.acc_mag.getHeading()
        return heading
    
class GPS():
    
    def __init__(self):
        self.gps = g()
    
    def read(self):
        self.gps.getLatLong()
    
    def getLat(self):
        return self.gps.lat
    
    def getLong(self):
        return self.gps.long
    
#a = AccelerometerCompass()
#print(print("Heading %.3f degrees\n" %(a.getCompassHeading())))
