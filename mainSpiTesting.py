'''
This file contains helper functions that are used by Stage, StageSPI, as well as the main function
Last Modified: R. Nance 5/15/2018
#####################DO NOT EDIT BELOW INFORMATION##################################
Originating Branch: Master
Originally Created: R. Nance 12/2017
'''

from helper import *
from Stage import *
from StageSPI import *
from datetime import datetime
from Joystick import *
import pygame
import random
import smbus
import time


###############GLOBAL VARIABLES###################
controlMode = 'position'
################END GLOBAL VARIABLEs############


#constructors for the stages
xaxis = StageSPI(0, 0, 6000)
yaxis = StageSPI(0, 1, 6000)
zaxis = Stage(0x40, 6000, 1)

xlinearRangeMin = 0
xlinearRangeMax = 12000
xlinearRange = 12000
ylinearRangeMin = 0
ylinearRangeMax = 12000
ylinearRange = 12000
constrainedLinearRange = 12000

axes = [zaxis]#
# , yaxis, zaxis]

#locations = [xlocation, ylocation, zlocation]
refreshRate = 20000  # cant remember what this is used for but I know it is important. I think it has something to do
#with pygame
lastMillis = 0

pygame.init()  # Initialize all pygame modules
pygame.joystick.init()  # Initialize joystick module


joy = CustomJoystick('Logitech', 0)

def setControlMode(newControlMode):
    controlMode = newControlMode



def setBounds():
    """
    Sets the bounds for position mode.
    1. determine which stop the home position is closest to
    2. determine the distance from that stop and assign it to
    3. create an artificial box with sides equal to the distance to the closest stop
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
    boundries = [home[0], home[1], 12001 - home[0], 12001 - home[1]]
    #boundries = [home[0],  12000 - home[0]]
    constrainedLinearRange = min(boundries)


    #ylinearRangeMin = yaxis.home - scaledRange +100
    #ylinearRangeMax = yaxis.home + scaledRange -100


sensitivity = 50
while True:
    #setBounds()
    try:

        time.sleep(0.01)
        buttons = []
        buttons = joy.getButtons()
        scaleInput = joy.getThrottle()
        print(scaleInput)
        x = joy.getX()
        y = 1023 - joy.getY()
        print('X: ', x, 'Y', y)
        print(buttons)
        if len(buttons) != 0:
            for nums in range(buttons.count('Zup')):
                print('Theres a ZUP')
                zaxis.zMove(0, 200) # move up120 encoder counts
            for nums in range(buttons.count('Zdown')):
                print('Theres a zdonw')
                zaxis.zMove(1, 200) # move down some amount 120 encoder counts
            for nums in range(buttons.count('Home')):
                print('Setting home as current position')
                print('Previous Home: ', home)
                xaxis.setCurrentHome()
                yaxis.setCurrentHome()
                print('Current Home: ', home)

        # Main commands to tell the stage to go to a location descibed by the joystick.




        # deal with the Z axis


        home = [zaxis.home, yaxis.home, zaxis.home]
        boundries = [home[0], home[1], 12001 - home[0], 12001 - home[1]]
        constrainedLinearRange = min(boundries)
        scaledRange = mapval(scaleInput, 0, 100, 0, constrainedLinearRange)
        print(scaledRange)
        xlinearRangeMin = home[0] - scaledRange + 100
        xlinearRangeMax = home[0] + scaledRange - 100
        print('XlinMin', xlinearRangeMin)
        print('xlinmax', xlinearRangeMax)
        print('Ylinmin', ylinearRangeMin)
        print('ylimmax', ylinearRangeMax)
        print('ylinearrange', ylinearRange)
        print('xlinearRange', xlinearRange)

        xaxis.goToLocation(mapval(x, 0, 1023, xlinearRangeMin, xlinearRangeMax))
        print('Mapval', mapval(x, 0, 1023, xlinearRangeMin, xlinearRangeMax))
        yaxis.goToLocation(mapval(y, 0, 1023, ylinearRangeMin, ylinearRangeMax))
        print('mapval y ', mapval(y, 0, 1023, ylinearRangeMin, ylinearRangeMax))

    except KeyboardInterrupt:
        #xaxis.sendCommandNoVars('19')
        #temp = xaxis.bus.read_i2c_block_data(0x33, 0)
        print('temp', temp)
        #xaxis.sendCommandNoVars('10')
        #temp = xaxis.bus.read_i2c_block_data(0x33, 0)
        print('temp', temp)
        f = open('errorLog.txt', 'a')
        f.write('\n' + 'Keyboard Inturrupt on '+str(datetime.now()))
        f.write(str(temp))
        f.close()
        print('Completed')
        raise
    '''
    except IOError:
        #xaxis.sendCommandNoVars('19')
        #temp = xaxis.bus.read_i2c_block_data(0x32, 0)
        #print('temp', temp)
        xaxis.sendCommandNoVars('10')
        temp = xaxis.bus.read_i2c_block_data(0x33, 0)
        print('temp', temp)
        f = open('errorLog.txt', 'a')
        f.write('\n' + 'Error Occured on '+ str(datetime.now()))
        #f.write(str(temp))
        raise
        #f.close()

    '''


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