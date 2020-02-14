import math
import geopy.distance


#PseudoCode for thrust direction. This will first require the accelerometer for headings.
def setThrustDirection(currentHeading, goToCoordsY, goToCoordsX, latitude, longitude, ServoX, ServoY):
    goToHeading = 180 * (math.atan2(goToCoordsY - longitude, goToCoordsX - latitude)) / math.pi
    
    theta = goToHeading - currentHeading
    
    theta = theta * (math.pi / 180)
    
    #thrustVectorX = 30 * math.sin(theta)
    #thrustVectorY = 30 * math.cos(theta)
    
    thrustVectorX = 30 * math.sin(theta)
    thrustVectorY = 30 * math.cos(theta)
    
    #thrustVectorX = (((thrustVectorX - 0) * (115 - 75)) / (360 - 0)) + 75
    #thrustVectorY = (((thrustVectorY - 0) * (115 - 75)) / (360 - 0)) + 75
    
    ServoX.move(thrustVectorX)
    ServoY.move(thrustVectorY)
    
def setThrustSpeed(goToCoordsY, goToCoordsX, pid, longitude, latitude, ESC):
    
    coords1 = (goToCoordsX, goToCoordsY)
    coords2 = (latitude, longitude)
    
    print(coords1, coords2)

    distMeters = geopy.distance.distance(coords1, coords2).m
    
    print(distMeters)

    output = abs(pid(distMeters))
    
    print(output)

    #NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
    output = (((output - 0) * (1000 - 2000)) / (100 - 0)) + 2000
    #output = abs(output)
    
    print(output)
    
    ESC.setSpeed(output)
