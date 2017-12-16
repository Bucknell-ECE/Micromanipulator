import pygame
from Joystick import *
import time


logitech_joystick = pygame.joystick.Joystick(0) # Create a new joystick. The id argument must be a value from 0 to pygame.joystick.get_count()-1.
logitech_joystick.init() # Initialize logitech_joystick
print logitech_joystick.get_init() # Initialize joystick
print logitech_joystick.get_id() # Get joystick ID
myname =  logitech_joystick.get_name() # Get joystick system name
print myname
numberaxes =  logitech_joystick.get_numaxes() # Get number of axes on joystick
print numberaxes
numberbuttons = logitech_joystick.get_numballs() # Get number of track balls logitech_joystick.get_numbuttons() # Get number of buttons on the joystick
print numberbuttons
print logitech_joystick.get_numhats() # Get number of hat controls

joy = CustomJoystick('Logitech')
while True:
    print'Throttle', joy.getThrottle()
    print'X: ', joy.getX()
    print'y ', joy.getY()
    time.sleep(.5)
