import pygame
from Joystick import *
import time

joy = CustomJoystick('Logitech')
while True:
    print'Throttle', joy.getThrottle()
    print'X: ', joy.getX()
    time.sleep(.5)
