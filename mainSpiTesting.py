from helper import *
from Stage import *
from StageSPI import *
from datetime import datetime
from Joystick import *
import pygame
import random
import smbus
import time
import spidev

#xaxis = Stage(0x33, 6000, 1)
#yaxis = Stage(0x40, 6000, 1)

xaxis = StageSPI(0, 0, 6000, 'zaxis')
yaxis = StageSPI(0, 1, 6000, 'yaxis')
zaxis = Stage(0x40, 6000, 1)
#xaxis.sendCommandNoVars('08')
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
axes = [zaxis]#
# , yaxis, zaxis]
home = [zaxis.home]#, yaxis.home, zaxis.home]
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


    #ylinearRangeMin = yaxis.home - scaledRange +100
    #ylinearRangeMax = yaxis.home + scaledRange -100


sensitivity = 50
while True:
    #setBounds()
    try:
        ###value = random.randrange(200,300,1)
        ###print(value)
        #xaxis.goToLocation(mapval(value, 0, 1023, 100, 11900))  # xlinearRangeMin, xlinearRangeMax))
        #print(datetime.now())
        #xaxis.sendCommandNoVars('03')
       # currentThrottle = joy.getThrottle()
        #if currentThrottle != zaxisOld:
            #if currentThrottle - zaxisOld > 0:
                #move up
        #print(joy.getButtons())



        time.sleep(0.01)
        buttons = []
        buttons = joy.getButtons()
        scaleInput = joy.getThrottle()
        x = joy.getX()
        y = joy.getY()
        print(buttons)
        if len(buttons) != 0:
            for nums in range(buttons.count('Zup')):
                print('Theres a ZUP')
                #zaxis.sendCommand('06 1', [48,48,48,48,48,48,55,56])
                zaxis.zMove(0, 200)
                #move up120 encoder counts

            for nums in range(buttons.count('Zdown')):
                print('Theres a zdonw')
                #zaxis.sendCommand('06 0', [48, 48, 48, 48, 48, 48, 55, 56])
                zaxis.zMove(1, 200)


                #move down some amount 120 encoder counts

        #print(joy.getAbsoluteThrottle())
        #print(joy.getThrottle())


        xaxis.goToLocation(mapval(x, 0, 1023, xlinearRangeMin, xlinearRangeMax))


        #yaxis.goToLocation(mapval(joy.getY(), 0, 1023, 100, 11900))


        #deal with the Z axis
        scaledRange = mapval(scaleInput, 0, 100, 0, constrainedLinearRange)
       # print('Scaled Range = ' , scaledRange)
        boundries = [home[0], 12000 - home[0]]
        constrainedLinearRange = min(boundries)
        #print('crange',constrainedLinearRange)
        xlinearRangeMin = xaxis.home - scaledRange + 100
        xlinearRangeMax = xaxis.home + scaledRange - 100
       # print('XlinMin', xlinearRangeMin)
        #print('xlinmax', xlinearRangeMax)


        ########print(joy.getX())
        #time.sleep(0.01)
       # xaxis.sendCommandNoVars('03')
        #time.sleep(0.01)
        #print('passed')
        # yaxis.goToLocation(mapval(joy.gety(), 0, 255, ylinearRangeMin, ylinearRangeMax))
        #print(time.time())
        #print(datetime.now())
        #time.sleep(0.0001)
        ###time.sleep(0.1)
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