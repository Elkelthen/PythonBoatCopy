import math


#PseudoCode for thrust direction. This will first require the accelerometer for headings.
def setThrustDirection(currentHeading, goToCoordsY, goToCoordsX, latitude, longitude, ServoX, ServoY):
    goToHeading = 180 * (math.atan2(goToCoordsY - longitude, goToCoordsX - latitude)) / math.pi
    
    theta = goToHeading - currentHeading
    
    theta = theta * (math.pi / 180)
    
    #thrustVectorX = 30 * math.sin(theta)
    #thrustVectorY = 30 * math.cos(theta)
    
    thrustVectorX = 31 * math.sin(theta)
    thrustVectorY = 31 * math.cos(theta)
    
    ServoX.move(thrustVectorX)
    ServoY.move(thrustVectorY)
    
def setThrustSpeed(goToCoordsY, goToCoordsX, pid, longitude, latitude, ESC):
    directionVectorX = goToCoordsX - latitude
    directionVectorY = goToCoordsY - longitude
    
    distanceFromWaypoint = math.sqrt(math.pow(directionVectorX, 2) + math.pow(directionVectorY, 2))
    
    print(distanceFromWaypoint)

    output = abs(pid(distanceFromWaypoint))
    
    print(output)
    
    if output > 100:
        output = 100
        
    print(output)
    
    #NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
    output = (((output - 0) * (2500 - 500)) / (100 - 0)) + 500
    
    print(output)
    
    ESC.setSpeed(output)