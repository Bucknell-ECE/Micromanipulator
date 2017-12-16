import pygame
from Joystick import *
import time

joy = CustomJoystick('Logitech')
while True:
    print'Throttle', joy.getThrottle()
    print'X: ', joy.getX()
    print'y ', joy.getY()
    time.sleep(.5)
