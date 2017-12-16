import pygame
from Joystick import *
import time

pygame.init() # Initialize all pygame modules
pygame.joystick.init() # Initialize joystick module


joy = CustomJoystick('Logitech', 0)


def getButtons():
    ###
    #pygame.init()
    #pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    pygame.event.get()
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    ###
    print('events being called')
    commands = []
    print pygame.event.get()
    for event in pygame.event.get():  # User did something
        print(event)
        if event.type == pygame.JOYBUTTONUP:
            button = event.button
            print("Button {} off".format(button))
    return commands
while True:

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
    '''
    joystick_count = pygame.joystick.get_count()
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        axes = joystick.get_numaxes()
        print("Number of axes: {}".format(axes))


        for i in range(axes):
            axis = joystick.get_axis(i)
            print("Axis {} value: {:>6.3f}".format(i, axis))

    '''
    print'Throttle', joy.getThrottle()
    print'X: ', joy.getX()
    print'y ', joy.getY()
    print'position', joy.getPosition()
    print'Buttons: ', getButtons()
    print'butt :', joy.getButtons()
    print'-----------------------------'
    print'absolute postion' , joy.getAbsolutePosition()

    time.sleep(1)
