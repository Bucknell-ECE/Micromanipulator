import pygame
from Joystick import *
import time

pygame.init() # Initialize all pygame modules
pygame.joystick.init() # Initialize joystick module

'''
print pygame.joystick.get_count() # Return number of joysticks
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
'''
#joy = CustomJoystick('Logitech')
while True:
    '''positionX = logitech_joystick.get_axis(0)
    positionY = logitech_joystick.get_axis(1)
    positionZ = logitech_joystick.get_axis(2)
    currentButton = logitech_joystick.get_button(6)
    button8 = logitech_joystick.get_button(7)
    button9 = logitech_joystick.get_button(8)
    button10 = logitech_joystick.get_button(9)
    button11 = logitech_joystick.get_button(10)
    print positionX  # Get current position of an axis
    print positionY
    print positionZ
'''
    '''
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")
    '''
    pygame.event.get()
    joystick_count = pygame.joystick.get_count()
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        axes = joystick.get_numaxes()
        print("Number of axes: {}".format(axes))


        for i in range(axes):
            axis = joystick.get_axis(i)
            print("Axis {} value: {:>6.3f}".format(i, axis))


    #print'Throttle', joy.getThrottle()
   # print'X: ', joy.getX()
    #print'y ', joy.getY()
    time.sleep(.5)
