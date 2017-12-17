import pygame
from Joystick import *
import time

pygame.init() # Initialize all pygame modules
pygame.joystick.init() # Initialize joystick module


joy = CustomJoystick('Logitech', 0)


def getButtons():
    ###
    # pygame.init()
    # pygame.joystick.init()
    #joystick = pygame.joystick.Joystick(0)
    #joystick.init()
    # Used to manage how fast the screen updates
    #clock = pygame.time.Clock()
    ###
    print('buttton static call')
    commands = ['pp']
    for event in pygame.event.get():  # User did something
        if event.type == pygame.JOYBUTTONUP:
            button = event.button
            print("Button {} off".format(button))
            commands += [button]

    '''        
    for event in pygame.event.get():  # User did something
        print(event)
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            # print("Joystick button pressed.")
            button = event.button
            print('button num ', button)
            print(buttonMap[button])
            commands += buttonMap[button]
            print(event)
        #if event.type == pygame.JOYBUTTONUP:
            # print("Joystick button released.")
           # print(event)
            # print(event.type)
            # print(event.button)
           # button = event.button
           # print("Button {} off".format(button))
          #  if button == 2:
          #      button2count += 1
        #print('Button 2 Coutnt is : ', button2count)
        clock.tick(20)
    '''
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
    #pygame.event.get()
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
    print'X: ', joy.getX()
    print'butt :', joy.getButtons()
    #print'Buttons: ', getButtons()

    #print'Throttle', joy.getThrottle()
    '''
    for event in pygame.event.get():  # User did something
        if event.type == pygame.JOYBUTTONUP:
            button = event.button
            print("Button {} off".format(button))
    '''

    print'y ', joy.getY()
    print'position', joy.getPosition()


    print'-----------------------------'
    print'absolute postion' , joy.getAbsolutePosition()

    time.sleep(1)
