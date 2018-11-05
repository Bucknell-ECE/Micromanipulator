# unused (7/5/18)

import pygame
from Joystick import *
import time

pygame.init() # Initialize all pygame modules
pygame.joystick.init() # Initialize joystick module


joy = CustomJoystick('Logitech', 0)

while True:

    print'butt :', joy.get_buttons()
    print'X: ', joy.get_x()
    print'y ', joy.get_y()
    print'position', joy.get_position()
    print'-----------------------------'
    print'absolute postion' , joy.get_absolute_position()

    time.sleep(1)
