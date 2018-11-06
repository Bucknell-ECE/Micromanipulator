'''
This file contains the functions that the joytick uses.
Last Modified: R. Nance 5/15/2018
#####################DO NOT EDIT BELOW INFORMATION##################################
Originating Branch: Joystick
Originally Created: R. Nance 12/2017
'''

from pygame import *
from helper import *



x_axis_NUM = 0
y_axis_NUM = 1
throttle_axis_NUM = 2

button_map = {
    1: 'z_down',
    2: 'z_up',
    3: 'Home',
    4: 'change_mode',
    6: 'get_status',
    7: 'Z Sensitivity Up',
    8: 'Z Sensitivity Down',
    9: 'Reset_home'
}

class CustomJoystick:
    # FIXME Will need to create a button mapping function that imports text file stuff here.

    def __init__(self, name, number):
        self.name = name
        self.joystick = pygame.joystick.Joystick(number)
        pygame.init()

        # Used to manage how fast the screen updates
        self.clock = pygame.time.Clock()

        # Initialize the joysticks
        pygame.joystick.init()

        joystick_count = pygame.joystick.get_count()
        joystick = pygame.joystick.Joystick(0)

        # For each joystick:
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            #print('this is joystick: ', i)
            joystick.init()
        axes = joystick.get_numaxes()
        #print(axes)


    def get_axis_position(self, axis_index):
        joystick = pygame.joystick.Joystick(0)
        return joystick.get_axis(axis_index)


    def convertPosition(self, axis_index):
        curr_pos = self.get_axis_position(axis_index)
        new_pos = (curr_pos + 1)*127.5  # TODO What's going on here?
        return new_pos



############################CODE WRITTEN BY RYDER#########################################
    def get_buttons(self):

        commands = []

        for event in pygame.event.get():  # User did something
            #print(event)
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop

            # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
            # TODO Verify these options with pygame documentation.
            if event.type == pygame.JOYBUTTONDOWN:
                button = event.button
                #commands += button
                commands += [button_map[button]]
            clock.tick(20)

        return commands


    def get_absolute_x(self):
        pygame.event.get()

        #joystick = pygame.joystick.Joystick(0)

        return self.joystick.get_axis(x_axis_NUM)


    def get_absolute_y(self):
        pygame.event.get()

        #joystick = pygame.joystick.Joystick(0)

        return self.joystick.get_axis(y_axis_NUM)


    def get_absolute_throttle(self):
        pygame.event.get()

        #joystick = pygame.joystick.Joystick(0)

        return self.joystick.get_axis(throttle_axis_NUM)


    def get_absolute_position(self):
        pygame.event.get()
        position = [round(self.joystick.get_axis(x_axis_NUM), 3), round(self.joystick.get_axis(y_axis_NUM), 3)]
        return position


    def get_x(self):
        pygame.event.get()

        #joystick = pygame.joystick.Joystick(0)

        absolute_x = self.get_absolute_x() + 1
        return map_val(absolute_x, 0, 2, 0, 2000)


    def get_y(self):
        pygame.event.get()

        #joystick = pygame.joystick.Joystick(0)

        absolute_y = self.get_absolute_y() + 1
        return map_val(absolute_y, 0, 2, 0, 2000)


    def get_throttle (self):
        pygame.event.get()

        absolute_throttle = self.get_absolute_throttle()
        return map_val(absolute_throttle, -1, 1, 0, 100)


    def get_position(self):
        pygame.event.get()

        absolute_position = [self.get_absolute_x() + 1, self.get_absolute_y() + 1]
        return map(lambda x: map_val(x, 0, 2, 0, 2000), absolute_position)
