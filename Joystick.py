'''
This file contains the functions that the joytick uses.
Last Modified: R. Nance 5/15/2018
#####################DO NOT EDIT BELOW INFORMATION##################################
Originating Branch: Joystick
Originally Created: R. Nance 12/2017
'''

import pygame
from helper import *

X_AXIS_NUM = 0
Y_AXIS_NUM = 1
THROTTLE_AXIS_NUM = 2

button_map = {
    0: 'null',
    1: 'z_down',
    2: 'z_up',
    3: 'Set Home',
    4: 'change_mode',
    6: 'get_status',
    7: 'decrease_scale_factor',
    8: 'increase_scale_factor',
    9: 'Reset Home',
    10: 'null'
}

# pygame returns buttons from raspi's config utility (that you download with pygame library)
# joystick.gtk? (used to configure buttons on joystick)


class CustomJoystick:

    def __init__(self, name, number):
        self.name = name
        self.joystick = pygame.joystick.Joystick(number)
        pygame.init()

        # Pygame clock is used to manage how fast the screen updates
        self.clock = pygame.time.Clock()

        # Initialize pygame's joystick modules
        pygame.joystick.init()

        joystick_count = pygame.joystick.get_count()
        joystick = pygame.joystick.Joystick(0)

        # For each joystick axis:
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            # print('this is joystick: ', i)
            joystick.init()
        axes = joystick.get_numaxes()  # remove assignment later

        # Set the options for the scale factor
        self.scale_factor_options = [1, 5, 10, 25, 50, 100]

        #  Associate INITIAL_SCALE with largest scale factor (100)
        self.input_scale_factor = self.scale_factor_options[-1]

        # Initialize value for scale_index
        self.scale_index = len(self.scale_factor_options) - 1


    def get_buttons(self):
        """
        Retrieves the full list of buttons and their respective status from the joystick.
        :return: commands for the M3-LS stages (processed in main.py loop)
        """
        clock = pygame.time.Clock()  # Create function-specific clock to poll for button input.
        commands = []

        for event in pygame.event.get():  # User did something!
            # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
            if event.type == pygame.JOYBUTTONDOWN:  # add to "commands" when a button is pressed
                button = event.button
                commands += [button_map[button]]

            clock.tick(60)  # Allows pygame to call event.get() 60 times per second.

        return commands


    def get_x(self):
        """Takes in the current position of the joystick x-axis, which ranges from -1 to 1 with a value of 0 being centered.
        :return: integer that denotes the number of encoder counts from the stage's zero-boundary
        """
        pygame.event.get()
        absolute_x = self.joystick.get_axis(X_AXIS_NUM)

        return map_val(absolute_x, -1, 1, 0, 12000)


    def get_y(self):
        """Takes in the current position of the joystick y-axis, which ranges from -1 to 1 with a value of 0 being centered.
        :return: integer that denotes the number of encoder counts from the stage's zero-boundary
        """
        pygame.event.get()
        absolute_y = self.joystick.get_axis(Y_AXIS_NUM)

        return map_val(absolute_y, -1, 1, 0, 12000)


    def decrease_scale_factor(self):
        if self.scale_index == 0:
            return
        else:
            self.scale_index -= 1
            self.input_scale_factor = self.scale_factor_options[self.scale_index - 1]


    def increase_scale_factor(self):
        if self.scale_index == len(self.scale_factor_options):
            return
        else:
            self.scale_index += 1
            self.input_scale_factor = self.scale_factor_options[self.scale_index - 1]


    def scaled_velocity_input(self, axis_num):
        """
        Scales the joystick displacement (type?) by input_scale_factor (int). Returns scaled_input_step (decimal int) for controlling velocity mode in main() loop.
        :return: scaled_input_step
        """
        # self.joystick.get_axis(axis_num) =

    # def get_throttle(self):  # Currently unused. Maybe use to help the user lower the needle to the desired height via the z-axis?
    #     pygame.event.get()
    #     absolute_throttle = self.joystick.get_axis(THROTTLE_AXIS_NUM)
    #
    #     return  # NUMBER