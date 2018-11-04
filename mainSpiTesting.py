## unused (7/5/18)

'''

This file contains testing information for the SPI stuff.
Last Modified: R. Nance 5/15/2018
#####################DO NOT EDIT BELOW INFORMATION##################################
Originating Branch: SPI_DevLocal

Originally Created: R. Nance 12/2017
'''

from helper import *
from Stage import *
from StageSPI import *
from StageI2C import *

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
x_axis = StageSPI(0, 0, 6000)
y_axis = StageSPI(0, 1, 6000)
z_axis = Stage(0x40, 6000, 1)

x_linear_range_min = 0
x_linear_range_max = 12000
xlinearRange = 12000
y_linear_range_min = 0
y_linear_range_max = 12000
ylinearRange = 12000
constrainedLinearRange = 12000

axes = [z_axis]#
# , y_axis, z_axis]

#locations = [xlocation, ylocation, zlocation]
REFRESH_RATE = 20000  # cant remember what this is used for but I know it is important. I think it has something to do
#with pygame
lastMillis = 0

pygame.init()  # Initialize all pygame modules
pygame.joystick.init()  # Initialize joystick module


joy = CustomJoystick('Logitech', 0)

def setControlMode(newControlMode):
    controlMode = newControlMode



def set_bounds():
    """
    Sets the bounds for position mode.
    1. determine which stop the home position is closest to
    2. determine the distance from that stop and assign it to
    3. create an artificial box with sides equal to the distance to the closest stop
    4. scale the constrainedRange between based on the position of the throttle
    5. Set LinearRangeMin values to home position - constrainedRange and max values to home position + constrainedRange
    :return: na
    """
    global x_linear_range_min
    global x_linear_range_max
    global y_linear_range_min
    global y_linear_range_max
    global constrainedLinearRange

    # Find which stop the stage is closest to
    # [left, bottom, right, top]
    boundries = [home[0], home[1], 12001 - home[0], 12001 - home[1]]
    #boundries = [home[0],  12000 - home[0]]
    constrainedLinearRange = min(boundries)


    #y_linear_range_min = y_axis.home - scaledRange +100
    #y_linear_range_max = y_axis.home + scaledRange -100


sensitivity = 50
while True:
    #set_bounds()
    try:

        time.sleep(0.01)
        buttons = []
        buttons = joy.get_buttons()
        scale_input = joy.get_throttle ()
        print(scale_input)
        x = joy.get_x()
        y = 1023 - joy.get_y()
        print('X: ', x, 'Y', y)
        print(buttons)
        if len(buttons) != 0:
            for nums in range(buttons.count('Zup')):
                print('Theres a ZUP')
                z_axis.z_move(0, 200) # move up120 encoder counts
            for nums in range(buttons.count('Zdown')):
                print('Theres a zdonw')
                z_axis.z_move(1, 200) # move down some amount 120 encoder counts
            for nums in range(buttons.count('Home')):
                print('Setting home as current position')
                print('Previous Home: ', home)
                x_axis.set_current_home()
                y_axis.set_current_home()
                print('Current Home: ', home)

        # Main commands to tell the stage to go to a location descibed by the joystick.




        # deal with the Z axis

        print('Starting Loop')
        home = [z_axis.home, y_axis.home, z_axis.home]
        print('Homes', home)
        boundries = [home[0], home[1], 12001 - home[0], 12001 - home[1]]
        print('boundries: ', boundries)
        constrainedLinearRange = min(boundries)
        print('constrainedlinearrange', constrainedLinearRange)
        scaledRange = map_val(scale_input, 0, 100, 0, constrainedLinearRange)
        print('Scaled Range: ', scaledRange)
        x_linear_range_min = home[0] - scaledRange + 100
        x_linear_range_max = home[0] + scaledRange - 100
        print('XlinMin', x_linear_range_min)
        print('xlinmax', x_linear_range_max)
        print('Ylinmin', y_linear_range_min)
        print('ylimmax', y_linear_range_max)
        print('ylinearrange', ylinearRange)
        print('xlinearRange', xlinearRange)

        x_axis.go_to_location(map_val(x, 0, 1023, x_linear_range_min, x_linear_range_max))
        print('map_val', map_val(x, 0, 1023, x_linear_range_min, x_linear_range_max))
        y_axis.go_to_location(map_val(y, 0, 1023, y_linear_range_min, y_linear_range_max))
        print('map_val y ', map_val(y, 0, 1023, y_linear_range_min, y_linear_range_max))

    except KeyboardInterrupt:
        #x_axis.send_command_no_vars('19')
        #temp = x_axis.bus.read_i2c_block_data(0x33, 0)
        print('temp', temp)
        #x_axis.send_command_no_vars('10')
        #temp = x_axis.bus.read_i2c_block_data(0x33, 0)
        print('temp', temp)
        f = open('errorLog.txt', 'a')
        f.write('\n' + 'Keyboard Inturrupt on '+str(datetime.now()))
        f.write(str(temp))
        f.close()
        print('Completed')
        raise
    '''
    except IOError:
        #x_axis.send_command_no_vars('19')
        #temp = x_axis.bus.read_i2c_block_data(0x32, 0)
        #print('temp', temp)
        x_axis.send_command_no_vars('10')
        temp = x_axis.bus.read_i2c_block_data(0x33, 0)
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
    if currentMillis - lastMillis < REFRESH_RATE:
        x = 1
        print('l', lastMillis)
        print(currentMillis)
    else:
        print('running')
        lastMillis = currentMillis
        #if controlMode == 'velocity':
            #fsdjfl
        if controlMode == 'position':
            set_bounds()

            x_axis.go_to_location(map_val(joy.get_x(), 0, 1023,100, 11900))# x_linear_range_min, x_linear_range_max))
            #y_axis.go_to_location(map_val(joy.get_y(), 0, 255, y_linear_range_min, y_linear_range_max))

            #time.sleep(0.1)
    '''