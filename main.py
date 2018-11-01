"""
This file contains the main loop to be run

Last Modified: Zheng Tian 6/29/2018
#####################DO NOT EDIT BELOW INFORMATION##################################
Originating Branch: Master
Originally Created: R. Nance 12/2017
"""

from helper import *
from Stage import *
from StageSPI import StageSPI
from StageI2C import StageI2C
from Joystick import *
from main_parameters import *  # May be a temporary file just for housekeeping.

from datetime import datetime
from tkinter import * ## was originally "Tkinter"
import pygame
import random
import time
import signal
import os.path
import subprocess
import threading

# Constructors for the stages
x_axis = StageSPI(0, 0, 6000)
y_axis = StageSPI(0, 1, 6000)

z_axis = StageI2C(0x40, 6000, 1)

x_axis.startup()  # Runs calibration sequences for each stage (in Stage.py).
y_axis.startup()
#z_axis.startup()  # TODO May want to uncomment this so we can calibrate z-motion.


if os.path.getsize('/home/pi/Micromanipulator/sensitivity.txt') > 0:
    scaleInput = sensitivity_read()
print('test', scaleInput)
#time.sleep(5)

x = 1000  # TODO What the heck are these? Are they constants, or variables?
y = 1000

x_coordinate = 1000  # TODO Should this be placed in the __init__ constructor?
y_coordinate = 1000
#locations = [xlocation, ylocation, zlocation]
REFRESH_RATE = 20000  # cant remember what this is used for but I know it is important. I think it has something to do
#with pygame  -- (Ryder)
lastMillis = 0


## Joystick initialization block
pygame.init()  # Initialize all pygame modules
pygame.joystick.init()  # Initialize joystick module

joy = CustomJoystick('Logitech', 0)
elapsed = 0
count = 0


def setControlMode(newControlMode):  # TODO This can be changed through Tony's code at bottom of this file.
    controlMode = newControlMode


# print('test',x_axis.sendCommand('40',hextocommand('001400')+[32]+hextocommand('00000A')+[32]+hextocommand('000033')+[32]+hextocommand1('0001')))
x_axis.sendCommand('40',hextocommand('000200')+[32]+hextocommand('00000A')+[32]+hextocommand('00000C')+[32]+hextocommand4('0001'))
y_axis.sendCommand('40',hextocommand('000200')+[32]+hextocommand('00000A')+[32]+hextocommand('00000C')+[32]+hextocommand4('0001'))
# 'Set CL speed to 200 ct/int'vl, [SPACE], minimum cutoff speed of 10 ct/int'vl, motor accel. of 12 ct/int'vl, int'vl dur. = 1
## Setting closed-loop speeds (C&C Ref. Guide, p. 19)
# TODO Make it so that these settings can be changed manually through the RPi terminal.


def main():
    global scaleInput
    global x
    global y
    global x_status
    global y_status
    global z_status
    global x_coordinate
    global y_coordinate
    global Zsensitivity

    try:  ## Loop for mapping joystick movements to M3-LS commands

        # print('x_axis location',x_axis.getPositionFromM3LS()), location in 12000
        # print('go to location test', x_axis.sendCommand('08', encodeToCommand(3000)))
        # print('command test', x_axis.sendCommand('06', [48] + [32] + encodeToCommand(100)))
        # Test result: <06 0 00000064>\r

        time.sleep(0.01)  # Delay for 10 ms so as not to overload SPI registers.
                          # TODO Can we decrease this to improve response time?
        buttons = []
        buttons = joy.getButtons()
        scaleInput = joy.getThrottle()
        print('Test Point 2',scaleInput)
        #time.sleep(2)
        sensitivitywrite(scaleInput)
        x = joy.getX()
        y = 2000 - joy.getY()
        #setBounds()
        print('X: ', x, 'Y', y)
        print(buttons)

        # print('X-axis closed-loop speed: ', x_axis.GetCloseLoopSpeed())
        # time.sleep(1)
        X = mapval(x, 0, 2000, xlinearRangeMin, xlinearRangeMax)
        Y = mapval(y, 0, 2000, ylinearRangeMin, ylinearRangeMax)
        #AudioNoti(X,Y,xlinearRangeMin,xlinearRangeMax,ylinearRangeMin,ylinearRangeMax)
        # print('Getstatus X', x_axis.getstatus())
        # print('Getstatus Z', z_axis.getstatus())
        if len(buttons) != 0:
            for nums in range(buttons.count('Zup')):
                print('Theres a ZUP')
                z_axis.zMove(0, Zsensitivity)  # move up120 encoder counts
            for nums in range(buttons.count('Zdown')):
                print('Theres a ZDOWN')
                z_axis.zMove(1, Zsensitivity)  # move down some amount 120 encoder counts
            for nums in range(buttons.count('Home')):
                print('Setting home as current position')
                x_axis.setCurrentHome()
                x_axis.setCurrentHome()
            for nums in range(buttons.count('ResetHome')):
                print('Reset home to the center of the stage')
                x_axis.goToLocation(6000)
                x_coordinate = 1000
                x_axis.goToLocation(6000)
                y_coordinate = 1000
            for nums in range(buttons.count('GetStatus')):
                getstatus = 1
                # statusx = x_axis.getstatus()
                # statusinfo(statusx)
                # statusy = x_axis.getstatus()
                # statusinfo(statusy)
                x_status = x_axis.getstatus()
                y_status = y_axis.getstatus()
                z_status = z_axis.getstatus()
                print('Getstatus X', x_status)
                print('Getstatus Y', y_status)
                print('Getstatus Z', z_status)
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

        # Main commands to tell the stage to go to a location described by the joystick.
        if x < 1000:
            x_axis.sendCommand('06', [48] + [32] + encodeToCommand(5))
            x_coordinate -= mapval(8,0,6000,0,2000)
            if x_coordinate <= 0:
                x_coordinate = 0
        elif x > 1000:
            x_axis.sendCommand('06', [49] + [32] + encodeToCommand(5))
            x_coordinate += mapval(8,0,12000,0,2000)
            if x_coordinate >= 2000:
                x_coordinate = 2000

        if y < 1000:
            x_axis.sendCommand('06', [48] + [32] + encodeToCommand(5))
            y_coordinate -= mapval(8,0,12000,0,12000)
        elif y > 1000:
            x_axis.sendCommand('06', [49] + [32] + encodeToCommand(5))
            y_coordinate += mapval(8,0,2000,0,12000)
        # x_axis.goToLocation(mapval(x, 0, 2000, xlinearRangeMin, xlinearRangeMax))
        # print('Mapval', mapval(x, 0, 2000, xlinearRangeMin, xlinearRangeMax))
        # x_axis.goToLocation(mapval(y, 0, 2000, ylinearRangeMin, ylinearRangeMax))
        # print('mapval y ', mapval(y, 0, 2000, ylinearRangeMin, ylinearRangeMax))

        #Move Open Loop Steps
        # x_axis.sendCommand('05', [49] + [32] + encodeToCommand4digit(100)+[32]+hextocommand4('186A')+[32]+hextocommand4('0C35'))
        # # x_axis.sendCommand('05', [49] + [32] + encodeToCommand4digit(1000))
        # time.sleep(0.2)
        # temp2 = x_axis.read()
        # print("This is feedback",temp2)

        # x_axis.sendCommandNoVars('52')
        # time.sleep(0.2)
        # temp3 = x_axis.read()
        # print("This is interval", temp3)

        #x_axis.sendCommand('05', [49] + [32] + encodeToCommand4digit(1000)+[32]+hextocommand4('186A')+[32]+hextocommand4('0C35'))

        # root=Tk()
        # positionx = Label(root, text = ('Postion x is ',x))
        # positionx.pack()
        # root.update_idletasks()

    except KeyboardInterrupt:
        # x_axis.sendCommandNoVars('19')
        # temp = x_axis.bus.read_i2c_block_data(0x33, 0)
        print('temp', temp)
        # x_axis.sendCommandNoVars('10')
        # temp = x_axis.bus.read_i2c_block_data(0x33, 0)
        print('temp', temp)
        f = open('errorLog.txt', 'a')
        f.write('\n' + 'Keyboard Interrupt on ' + str(datetime.now()))
        f.write(str(temp))
        f.close()
        print('Completed')
        raise

starttime = time.time()

while elapsed <= 1:
    main()
    # elapsed =  time.time() - starttime
    # count += 1
    # print('This is count',count)


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
#
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
#
#
# class myThread(threading.Thread):
#     def __init__(self, threadID, name, counter):
#         threading.Thread.__init__(self)
#         self.threadID = threadID
#         self.name = name
#         self.counter = counter
#     def run(self):
#         print("Starting" + self.name)
#         print_time(self.name, self.counter, 5)
#         print("Exiting" + self.name)
#
# def print_time(threadName, delay, counter):
#     while counter:
#         if exitFlag:
#             (threading.Thread).exit()
#         time.sleep(delay)
#         counter -= 1

# root = Tk(className = 'Micromanipulator')
# root.geometry("400x150")
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
#     positionx['text'] = ('Position x is ',x_coordinate)
#     positionx.pack()
#     positiony['text'] = ('Position y is ',y_coordinate)
#     positiony.pack()
#     sensitivity_scale['text'] = ('Sensitivity Percentage is ', scaleInput)
#     sensitivity_scale.pack()
#     statusx['text'] = ('x status is ', x_status)
#     statusx.pack()
#     statusy['text'] = ('y status is ', y_status)
#     statusy.pack()
#     statusz['text'] = ('z status is ', z_status)
#     statusz.pack()


'''
except IOError:
    #x_axis.sendCommandNoVars('19')
    #temp = x_axis.bus.read_i2c_block_data(0x32, 0)
    #print('temp', temp)
    x_axis.sendCommandNoVars('10')
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
        setBounds()

        x_axis.goToLocation(mapval(joy.getX(), 0, 1023,100, 11900))# xlinearRangeMin, xlinearRangeMax))
        #x_axis.goToLocation(mapval(joy.gety(), 0, 255, ylinearRangeMin, ylinearRangeMax))

        #time.sleep(0.1)
'''
