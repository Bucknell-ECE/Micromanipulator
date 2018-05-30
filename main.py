'''

This file contains the main loop to be run

Last Modified: R. Nance 5/15/2018
#####################DO NOT EDIT BELOW INFORMATION##################################
Originating Branch: Master
Originally Created: R. Nance 12/2017
'''

from helper import *
from Stage import *
from StageSPI import StageSPI
from StageI2C import StageI2C

from datetime import datetime
from Joystick import *
from Tkinter import *
import pygame
import random
import time


###############GLOBAL VARIABLES###################
controlMode = 'position'
safety_margin = 50
################END GLOBAL VARIABLEs############


#constructors for the stages
xaxis = StageSPI(0, 0, 6000)
yaxis = StageSPI(0, 1, 6000)

zaxis = StageI2C(0x40, 6000, 1)


xlinearRangeMin = 0
xlinearRangeMax = 12000
xlinearRange = 12000
ylinearRangeMin = 0
ylinearRangeMax = 12000
ylinearRange = 12000
constrainedLinearRange = 12000
sensitivity = 50
Zsensitivity = 200


#locations = [xlocation, ylocation, zlocation]
refreshRate = 20000  # cant remember what this is used for but I know it is important. I think it has something to do
#with pygame
lastMillis = 0

pygame.init()  # Initialize all pygame modules
pygame.joystick.init()  # Initialize joystick module

# root = Tk(className = 'Micromanipulator')
# root.after(0)
# root.mainloop()

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
    with a small offset for safety, so that the stages never run into the stops.

    ####TOT
    :return: na
    """
    global xlinearRangeMin
    global xlinearRangeMax
    global ylinearRangeMin
    global ylinearRangeMax
    global constrainedLinearRange
    global safty_margin


    print('Setting Linear Range')
    home = [xaxis.home, yaxis.home, zaxis.home]
    print('Homes', home)
    # Find which stop the stage is closest to
    # [left, bottom, right, top]
    boundries = [home[0], home[1], 12000 - home[0], 12000 - home[1]]
    print('boundries: ', boundries)
    constrainedLinearRange = min(boundries)
    print('constrainedlinearrange', constrainedLinearRange)
    scaledRange = mapval(scaleInput, 0, 100, 0, constrainedLinearRange)
    print('Scaled Range: ', scaledRange)
    xlinearRangeMin = home[0] - scaledRange + safety_margin
    xlinearRangeMax = home[0] + scaledRange - safety_margin
    ylinearRangeMin = yaxis.home - scaledRange + safety_margin
    ylinearRangeMax = yaxis.home + scaledRange - safety_margin


    print('XlinMin', xlinearRangeMin)
    print('xlinmax', xlinearRangeMax)
    print('Ylinmin', ylinearRangeMin)
    print('ylimmax', ylinearRangeMax)
    print('ylinearrange', ylinearRange)
    print('xlinearRange', xlinearRange)

    # x_status = xaxis.getstatus()
    # z_status = zaxis.getstatus()

    # xaxis.MotorDirection(x_status)
    # zaxis.MotorDirection(z_status)
    # xaxis.Running(x_status)
    # zaxis.Running(z_status)


while True:

    try:
        time.sleep(0.01)
        buttons = []
        buttons = joy.getButtons()
        scaleInput = joy.getThrottle()
        print(scaleInput)
        x = joy.getX()
        y = 2000 - joy.getY()
        setBounds()
        print('X: ', x, 'Y', y)
        print(buttons)
        X = mapval(x,0,2000,xlinearRangeMin,xlinearRangeMax)
        Y = mapval(y,0,2000,ylinearRangeMin,ylinearRangeMax)
        AudioNoti(X,Y,xlinearRangeMin,xlinearRangeMax,ylinearRangeMin,ylinearRangeMax)
        #print('Getstatus X', xaxis.getstatus())
        #print('Getstatus Z', zaxis.getstatus())
        if len(buttons) != 0:
            for nums in range(buttons.count('Zup')):
                print('Theres a ZUP')
                zaxis.zMove(0, Zsensitivity) # move up120 encoder counts
            for nums in range(buttons.count('Zdown')):
                print('Theres a ZDOWN')
                zaxis.zMove(1, Zsensitivity) # move down some amount 120 encoder counts
            for nums in range(buttons.count('Home')):
                print('Setting home as current position')
                xaxis.setCurrentHome()
                yaxis.setCurrentHome()
            for nums in range(buttons.count('ResetHome')):
                print('Reset home to the center of the stage')
                xaxis.setHome(6000)
                yaxis.setHome(6000)
            for nums in range(buttons.count('GetStatus')):
                print('Getstatus X', xaxis.getstatus())
                print('Getstatus Y', yaxis.getstatus())
                print('Getstatus Z', zaxis.getstatus())
            for nums in range(buttons.count('Z Sensitivity Up')):
                print('Z sensitivity up by 50, Now the sensitivity is',Zsensitivity)
                Zsensitivity += 50
            for nums in range(buttons.count('Z Sensitivity Down')):
                print('Z sensitivity up down 50, Now the sensitivity is', Zsensitivity)
                Zsensitivity -= 50

        # Main commands to tell the stage to go to a location descibed by the joystick.
        xaxis.goToLocation(mapval(x, 0, 2000, xlinearRangeMin, xlinearRangeMax))
        print('Mapval', mapval(x, 0, 2000, xlinearRangeMin, xlinearRangeMax))
        yaxis.goToLocation(mapval(y, 0, 2000, ylinearRangeMin, ylinearRangeMax))
        print('mapval y ', mapval(y, 0, 2000, ylinearRangeMin, ylinearRangeMax))

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