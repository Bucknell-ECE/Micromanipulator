'''
This file contains the functions that the joytick uses.
Last Modified: R. Nance 5/15/2018
#####################DO NOT EDIT BELOW INFORMATION##################################
Originating Branch: Joystick
Originally Created: R. Nance 12/2017
'''

import pygame
from helper import *

x_axis_NUM = 0
y_axis_NUM = 1
throttle_axis_NUM = 2

button_map = {
    0: 'null',
    1: 'z_down',
    2: 'z_up',
    3: 'Set Home',
    4: 'change_mode',
    6: 'get_status',
    7: 'Decrease scale_input',
    8: 'Increase scale_input',
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

        # Initialize the joystick
        pygame.joystick.init()

        # Count the joysticks
        joystick_count = pygame.joystick.get_count()

        self.scale_options = [1, 5, 10, 25, 50, 100]

        # TODO RYDER: How is this loop doing anything new?
        # For each joystick:
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()


    def get_buttons(self):
        clock = pygame.time.Clock()  # Create function-specific clock to poll for button input.
        commands = []

        for event in pygame.event.get():  # User did a thing!
            # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
            if event.type == pygame.JOYBUTTONDOWN:  # add to "commands" when a button is pressed
                button = event.button
                commands += [button_map[button]]

            clock.tick(20)  # TODO Why are we polling only every 20 ms? Can we try lower?
            # Tony's addition?

        return commands


    def get_absolute_x(self):
        """Returns the current position of a joystick axis. The value will
        range from -1 to 1 with a value of 0 being centered.
        :return:
        """
        pygame.event.get()

        return self.joystick.get_axis(x_axis_NUM)


    def get_absolute_y(self):
        pygame.event.get()

        return self.joystick.get_axis(y_axis_NUM)


    def get_absolute_throttle(self):
        pygame.event.get()

        return self.joystick.get_axis(throttle_axis_NUM)


    def get_absolute_position(self):
        position = [round(self.get_absolute_x(), 3), round(self.get_absolute_y(), 3)]

        return position


    def get_x(self):
        """
        Maps absolute_x into an integer between 0 and 2000.
        :return: integer that denotes the number of encoder counts from the stage's zero-boundary
        """
        absolute_x = self.get_absolute_x() + 1

        return map_val(absolute_x, 0, 2, 0, 2000)


    def get_y(self):
        """
        Maps absolute_y into an integer between 0 and 2000.
        :return: integer that denotes the number of encoder counts from the stage's zero-boundary
        """
        absolute_y = self.get_absolute_y() + 1
        return map_val(absolute_y, 0, 2, 0, 2000)


    def get_throttle(self):
        absolute_throttle = self.get_absolute_throttle()
        self.scale_input = map_val(absolute_throttle, -1, 1, 0, 100)

        return self.scale_input


    # Currently unused, possibly so that other functions can utilize constituent subfunctions.
    def get_position(self):
        absolute_position = [self.get_absolute_x() + 1, self.get_absolute_y() + 1]

        return map(lambda x: map_val(x, 0, 2, 0, 2000), absolute_position)
        # for reference:
        # map_val(x, in_min, in_max, out_min, out_max)
        # int(round((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min, 0))