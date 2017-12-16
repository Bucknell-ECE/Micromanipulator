import pygame
from Joystick import *

joy = CustomJoystick('Logitech')
while True:
    print'Throttle', joy.getThrottle()
    print'X: ', joy.getX()
