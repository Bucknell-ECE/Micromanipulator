import pygame
from Joystick import *
import time

pygame.init() # Initialize all pygame modules
pygame.joystick.init() # Initialize joystick module


joy = CustomJoystick('Logitech', 0)

while True:

    print'butt :', joy.getButtons()
    print'X: ', joy.getX()
    print'y ', joy.getY()
    print'position', joy.getPosition()
    print'-----------------------------'
    print'absolute postion' , joy.getAbsolutePosition()

    time.sleep(1)
