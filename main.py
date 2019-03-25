"""
This file contains the main loop to be run

Last Modified: Jacquelyn Scott, November 2018
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

from datetime import datetime, timedelta
from Tkinter import *
import pygame
import time
import signal
import os.path
import subprocess
import threading

# global input_scale_factor
global x
global y
global x_status
global y_status
global z_status
global x_coordinate
global y_coordinate
global z_sensitivity

# Constructors for the stages
x_axis = StageSPI(0, 0, 6000)  # open x-axis on bus 0
y_axis = StageSPI(0, 1, 6000)  # open y-axis on bus 1
z_axis = StageI2C(0x40, 6000, 1)  # TODO What does "@" symbol mean in an I2C address?

x_axis.startup()  # Runs calibration sequences for each stage (in Stage.py).
y_axis.startup()
#z_axis.startup()

#initialize time (can account for daylight savings time, DST) for logging purposes:
import time
t = time.time()
t_str = time.strftime('%Y-%m-%d %H:%M %Z', time.localtime(t))


# if os.path.getsize('/home/pi/Micromanipulator/sensitivity.txt') > 0:
#     input_scale_factor = sensitivity_read()
# print('test', input_scale_factor)
# #time.sleep(5)

# # "x" and "y" will be overwritten with the "joy.get_x() and ".get_y()" functions.
# x = 1000
# y = 1000
#
# x_coordinate = 1000
# y_coordinate = 1000

#locations = [xlocation, ylocation, zlocation]


# Initialize joysticks
pygame.init()  # Initialize all pygame modules
pygame.joystick.init()  # Initialize joystick module

joy = CustomJoystick('Logitech', 0)

# # print('test',x_axis.send_command('40',hex_to_command('001400')+[32]+hex_to_command('00000A')+[32]+hex_to_command('000033')+[32]+hex_to_command1('0001')))
# x_axis.send_command('40',hex_to_command('000200')+[32]+hex_to_command('00000A')+[32]+hex_to_command('00000C')+[32]+hex_to_command4('0001'))  # Prints command after running

# y_axis.send_command('40',hex_to_command('000200')+[32]+hex_to_command('00000A')+[32]+hex_to_command('00000C')+[32]+hex_to_command4('0001'))
# # 'Set CL speed to 200 ct/int'vl, [SPACE], minimum cutoff speed of 10 ct/int'vl, motor accel. of 12 ct/int'vl, int'vl dur. = 1
# # NOTE Setting closed-loop speeds (C&C Ref. Guide, p. 19)
# TODO Make it so that these settings can be changed manually through the RPi terminal.


def main():

    # print('All values in encoder counts (2 cts / micron).')

    # Set linear ranges depending on home position
    print(  'x_axis.home = 'x_axis.home,
            'y_axis.home = 'y_axis.home,
            'z_axis.home = 'z_axis.home)

    home = [x_axis.home, y_axis.home, z_axis.home]
    # print('Homes', home)
    # Find which stop the stage is closest to (in encoder counts)
    # [left, bottom, right, top]
    boundaries = [x_axis.home, y_axis.home, 12000 - x_axis.home, 12000 - y_axis.home]
    # print('boundaries: ', boundaries)

    # Take the smallest boundary value,
    constrained_linear_range = min(boundaries)
    # print('constrained_linear_range', constrained_linear_range)

    # ... and make a square out of that smallest value
    scaled_range = map_val(joy.input_scale_factor, 0, 100, 0, constrained_linear_range)
    # print('Scaled Range: ', scaled_range)

    x_linear_range_min = x_axis.home - scaled_range + safety_margin
    x_linear_range_max = x_axis.home + scaled_range - safety_margin
    y_linear_range_min = y_axis.home - scaled_range + safety_margin
    y_linear_range_max = y_axis.home + scaled_range - safety_margin


    #f1 = open('map_val-recording.txt', 'a')  # used for recording map_val outputs

    # Loop for mapping joystick movements to M3-LS commands
    try:

        time.sleep(0.01)  # 10 ms delay allows ample time for everything.

        # console_readout()

        buttons = joy.get_buttons()
        print('input_scale_factor = ', joy.input_scale_factor)
        print('scale_index = ', joy.scale_index, 'out of ', len(joy.scale_index))

        #
        x = joy.get_x()
        y = 12000 - joy.get_y()  # encoder counts
        print('Joystick X: ', x, 'Y: ', y)


        # Main commands to tell the stage to go to a location described by the joystick.
        mapped_x = map_val(x, 0, 12000, x_linear_range_min, x_linear_range_max)
        mapped_y = map_val(y, 0, 12000, y_linear_range_min, y_linear_range_max)

        x_axis.go_to_location(mapped_x)
        # print('map_val x: ', mapped_x)
        # f1.write('\n' + 'mapped range of x:' + str(mapped_x) + '\n')
        # f1.write(str(time.now()))

        y_axis.go_to_location(mapped_y)
        # print('map_val y: ', mapped_y)
        # f1.write('\n' + str(mapped_y) + '\n')

        # print('\n')  # line break

        # Code for acting upon button presses
        if len(buttons) != 0:
            # NOTE: 'for' statements return the no. of times a button mapping appears in the 'buttons' list. I have changed these to "if" statements to remove redundancy.

            if buttons.count('z_up') > 0:
                z_axis.z_move(1, z_sensitivity)  # move z-axis up by z_sensitivity

            if buttons.count('z_down') > 0:
                z_axis.z_move(0, z_sensitivity)  # move z-axis down by z_sensitivity

            if buttons.count('Set Home') > 0:
                x_axis.set_current_home()
                y_axis.set_current_home()
                # z_axis.set_current_home()

            if buttons.count('Reset Home') > 0:
                x_axis.set_home(6000)
                # x_coordinate = 6000
                y_axis.set_home(6000)
                # y_coordinate = 6000
                # z_axis.set_home(6000)

            if buttons.count('get_status') > 0:  # 'get_status' in 'buttons'

                x_status = x_axis.get_status()
                y_status = y_axis.get_status()
                z_status = z_axis.get_status()

                print('get_status X', x_status)
                print('get_status Y', y_status)
                print('get_status Z', z_status)

                while get_status == 1:
                    buttons = joy.get_buttons()
                    if buttons.count('get_status'):
                        get_status = 0
                        # signal.pause()

            if buttons.count('Decrease input_scale_factor') > 0:
                joy.decrease_scale_factor()

            if buttons.count('Increase input_scale_factor') > 0:
                joy.increase_scale_factor()

        ## Velocity mode
        if joy.get_x() > 6000:
            x_axis.send_command()


    except KeyboardInterrupt:
        # x_axis.send_command_no_vars('19')
        # temp = x_axis.bus.read_i2c_block_data(0x33, 0)
        # f1.close()
        raise


start_time = time.time()

elapsed = 0
count = 0

while True:
    main()
    # elapsed =  time.time() - start_time
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
#     sensitivity_scale['text'] = ('Sensitivity Percentage is ', input_scale_factor)
#     sensitivity_scale.pack()
#     statusx['text'] = ('x status is ', x_status)
#     statusx.pack()
#     statusy['text'] = ('y status is ', y_status)
#     statusy.pack()
#     statusz['text'] = ('z status is ', z_status)
#     statusz.pack()



# except IOError:
#     #x_axis.send_command_no_vars('19')
#     #temp = x_axis.bus.read_i2c_block_data(0x32, 0)
#     #print('temp', temp)
#     x_axis.send_command_no_vars('10')
#     temp = x_axis.bus.read_i2c_block_data(0x33, 0)
#     print('temp', temp)
#     f = open('errorLog.txt', 'a')
#     f.write('\n' + 'Error Occured on '+ str(datetime.now()))
#     #f.write(str(temp))
#     raise
#     #f.close()

