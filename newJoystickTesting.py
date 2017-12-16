import pygame
from Joystick import *

joy = CustomJoystick('Logitech')

print'Throttle', joy.getThrottle()
print'X: ', joy.getX()
