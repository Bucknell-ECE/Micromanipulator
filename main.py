'''

This file contains the main loop to be run

Last Modified: Zheng Tian 6/13/2018
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
import signal
import os.path

###############GLOBAL VARIABLES###################
controlMode = 'position'
safety_margin = 50
################END GLOBAL VARIABLEs############


#constructors for the stages
xaxis = StageSPI(0, 0, 6000)
yaxis = StageSPI(0, 1, 6000)

zaxis = StageI2C(0x40, 6000, 1)

xaxis.startup()
yaxis.startup()
#zaxis.startup()

xlinearRangeMin = 0
xlinearRangeMax = 12000
xlinearRange = 12000
ylinearRangeMin = 0
ylinearRangeMax = 12000
ylinearRange = 12000
constrainedLinearRange = 12000
sensitivity = 50
Zsensitivity = 200
getstatus = 0
scaleInput = 0
xstatus = ''
ystatus = ''
zstatus = ''

if os.path.getsize('/home/pi/Micromanipulator/sensitivity.txt') > 0:
    scaleInput = sensitivityread()
print('test',scaleInput)
#time.sleep(5)

x = 1000
y = 1000

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




def main():
    global scaleInput
    global x
    global y
    global xstatus
    global ystatus
    global zstatus

    try:
        # print('xaxis location',xaxis.getPositionFromM3LS()), location in 12000
        # print('go to location test', xaxis.sendCommand('08', encodeToCommand(3000)))
        # print('command test', xaxis.sendCommand('06', [48] + [32] + encodeToCommand(100)))
        # Test result: <06 0 00000064>\r
        time.sleep(0.01)
        buttons = []
        buttons = joy.getButtons()
        scaleInput = joy.getThrottle()
        print('Test Point 2',scaleInput)
        #time.sleep(2)
        sensitivitywrite(scaleInput)
        x = joy.getX()
        y = 2000 - joy.getY()
        setBounds()
        print('X: ', x, 'Y', y)
        print(buttons)
        X = mapval(x, 0, 2000, xlinearRangeMin, xlinearRangeMax)
        Y = mapval(y, 0, 2000, ylinearRangeMin, ylinearRangeMax)
        #AudioNoti(X,Y,xlinearRangeMin,xlinearRangeMax,ylinearRangeMin,ylinearRangeMax)
        # print('Getstatus X', xaxis.getstatus())
        # print('Getstatus Z', zaxis.getstatus())
        if len(buttons) != 0:
            for nums in range(buttons.count('Zup')):
                print('Theres a ZUP')
                zaxis.zMove(0, Zsensitivity)  # move up120 encoder counts
            for nums in range(buttons.count('Zdown')):
                print('Theres a ZDOWN')
                zaxis.zMove(1, Zsensitivity)  # move down some amount 120 encoder counts
            for nums in range(buttons.count('Home')):
                print('Setting home as current position')
                xaxis.setCurrentHome()
                yaxis.setCurrentHome()
            for nums in range(buttons.count('ResetHome')):
                print('Reset home to the center of the stage')
                xaxis.setHome(6000)
                yaxis.setHome(6000)
            for nums in range(buttons.count('GetStatus')):
                getstatus = 1
                # statusx = xaxis.getstatus()
                # statusinfo(statusx)
                # statusy = yaxis.getstatus()
                # statusinfo(statusy)
                xstatus = xaxis.getstatus()
                ystatus = yaxis.getstatus()
                zstatus = zaxis.getstatus()
                print('Getstatus X', xstatus)
                print('Getstatus Y', ystatus)
                print('Getstatus Z', zstatus)
                while getstatus == 1:
                    buttons = joy.getButtons()
                    if buttons.count('GetStatus'):
                        getstatus = 0
                        # signal.pause()
            for nums in range(buttons.count('Z Sensitivity Up')):
                print('Z sensitivity up by 50, Now the sensitivity is', Zsensitivity)
                Zsensitivity += 50
            for nums in range(buttons.count('Z Sensitivity Down')):
                print('Z sensitivity up down 50, Now the sensitivity is', Zsensitivity)
                Zsensitivity -= 50

        # Main commands to tell the stage to go to a location descibed by the joystick.
        xaxis.goToLocation(mapval(x, 0, 2000, xlinearRangeMin, xlinearRangeMax))
        print('Mapval', mapval(x, 0, 2000, xlinearRangeMin, xlinearRangeMax))
        yaxis.goToLocation(mapval(y, 0, 2000, ylinearRangeMin, ylinearRangeMax))
        print('mapval y ', mapval(y, 0, 2000, ylinearRangeMin, ylinearRangeMax))

        # root=Tk()
        # positionx = Label(root, text = ('Postion x is ',x))
        # positionx.pack()
        # root.update_idletasks()

    except KeyboardInterrupt:
        # xaxis.sendCommandNoVars('19')
        # temp = xaxis.bus.read_i2c_block_data(0x33, 0)
        print('temp', temp)
        # xaxis.sendCommandNoVars('10')
        # temp = xaxis.bus.read_i2c_block_data(0x33, 0)
        print('temp', temp)
        f = open('errorLog.txt', 'a')
        f.write('\n' + 'Keyboard Interrupt on ' + str(datetime.now()))
        f.write(str(temp))
        f.close()
        print('Completed')
        raise

# while True:
#     main()

#Refreshing Rate of 0.05s
# def exitTK():
#     global root
#     root.destroy()
#
# while True:
#     root=Tk()
#     main()
#     positionx = Label(root, text = ('Position x is ', x))
#     positionx.pack()
#     positiony = Label(root, text = ('Position y is ', y))
#     positiony.pack()
#     root.after(50,exitTK)
#     root.mainloop()

# class App(threading.Thread):
#     def __init__(self, tk_root):
#         self.root = tk_root
#         threading.Thread.__init__(self)
#         self.start()
#     def run(self):
#         loop_active = True
#         while loop_active:
#             user_input = raw_input("Command")
#             if user_input == 'exit':
#                 loop_active = False
#                 self.root.quit()
#                 self.root.update()
#             else:
#                 label = Label(self.root, text = user_input)
#                 label.pack()


# root = Tk(className = 'Micromanipulator')
# positionx = Label(root, text = "welcome")
# positiony = Label(root, text = "welcome")
# sensitivity_scale = Label(root, text = "welcome")
# exit = Button(root, text = "Quit", command = quit)
# statusx = Label(root, text = 'welcome')
# statusy = Label(root, text = 'welcome')
# statusz = Label(root, text = 'welcome')
# positionx.pack()
# positiony.pack()
# sensitivity_scale.pack()
# statusx.pack()
# statusy.pack()
# statusz.pack()
# exit.pack()
#
# def quit():
#     global root
#     root.quit()
#
# while True:
#     root.update()
#     main()
#     positionx['text'] = ('Position x is ',x)
#     positionx.pack()
#     positiony['text'] = ('Position y is ',y)
#     positiony.pack()
#     sensitivity_scale['text'] = ('Sensitivity Level is ', scaleInput)
#     sensitivity_scale.pack()
#     statusx['text'] = ('x status is ', xstatus)
#     statusx.pack()
#     statusy['text'] = ('y status is ', ystatus)
#     statusy.pack()
#     statusz['text'] = ('z status is ', zstatus)
#     statusz.pack()


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
