from helper import *
from Stage import *
from datetime import datetime
from Joystick import *
import pygame
xaxis = Stage(0x32, 6000, 1)
#yaxis = Stage(0x33, 6000, 1)
#zaxis = Stage(0x34, 6000, 1)
controlMode = 'position'
xlinearRangeMin = 0
xlinearRangeMax = 12000
xlinearRange = 12000
ylinearRangeMin = 0
ylinearRangeMax = 12000
ylinearRange = 12000
constrainedLinearRange = 12000
axes = [xaxis]#
# , yaxis, zaxis]
home = [xaxis.home]#, yaxis.home, zaxis.home]
#locations = [xlocation, ylocation, zlocation]
refreshRate = 20000
lastMillis = 0

pygame.init() # Initialize all pygame modules
pygame.joystick.init() # Initialize joystick module


joy = CustomJoystick('Logitech', 0)

def setControlMode(newControlMode):
    controlMode = newControlMode



def setBounds():
    """
    Sets the bounds for position mode.
    1. determine which stop the home position is closest to
    2. determine the distance from that stop and assign it to
    3. create an artificail box with sides equal to the distance to the closest stop
    4. scale the constrainedRange between based on the position of the throttle
    5. Set LinearRangeMin values to home position - constrainedRange and max values to home position + constrainedRange
    :return: na
    """
    global xlinearRangeMin
    global xlinearRangeMax
    global ylinearRangeMin
    global ylinearRangeMax
    global constrainedLinearRange

    # Find which stop the stage is closest to
    # [left, bottom, right, top]
    #boundries = [home[0], home[1], 12000 - home[0], 12000 - home[1]]
    boundries = [home[0],  12000 - home[0]]
    constrainedLinearRange = min(boundries)

    scaleInput = joy.getThrottle()

    scaledRange = mapval(scaleInput, 0, 1023, 0, constrainedLinearRange)


    xlinearRangeMin = xaxis.home - scaledRange +100
    xlinearRangeMax = xaxis.home + scaledRange -100
    #ylinearRangeMin = yaxis.home - scaledRange +100
    #ylinearRangeMax = yaxis.home + scaledRange -100


while True:
    #setBounds()

    #xaxis.goToLocation(mapval(joy.getX(), 0, 1023, 100, 11900))  # xlinearRangeMin, xlinearRangeMax))
    print(datetime.now())
    xaxis.goToLocation(mapval(500, 0, 1023, 100, 11900))  # xlinearRangeMin, xlinearRangeMax))
    #print('passed')
    # yaxis.goToLocation(mapval(joy.gety(), 0, 255, ylinearRangeMin, ylinearRangeMax))
    #print(time.time())
    #print(datetime.now())
    time.sleep(0.0001)
    '''
    #currentMillis = datetime.now().microsecond
    currentMillis = time.time() * 1000000
    if currentMillis - lastMillis < refreshRate:
        x = 1
        print('l', lastMillis)
        print(currentMillis)
    else:
        print('running')
        lastMillis = currentMillis
        #if controlMode == 'velocity':
            #fsdjfl
        if controlMode == 'position':
            setBounds()

            xaxis.goToLocation(mapval(joy.getX(), 0, 1023,100, 11900))# xlinearRangeMin, xlinearRangeMax))
            #yaxis.goToLocation(mapval(joy.gety(), 0, 255, ylinearRangeMin, ylinearRangeMax))

            #time.sleep(0.1)
    '''