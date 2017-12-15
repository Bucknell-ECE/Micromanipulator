import pygame
import sys
import time

pygame.init() # Initialize all pygame modules
pygame.joystick.init() # Initialize joystick module


print pygame.joystick.get_count() # Return number of joysticks

logitech_joystick = pygame.joystick.Joystick(0) # Create a new joystick. The id argument must be a value from 0 to pygame.joystick.get_count()-1.
logitech_joystick.init() # Initialize logitech_joystick
print logitech_joystick.get_init() # Initialize joystick
print logitech_joystick.get_id() # Get joystick ID
print logitech_joystick.get_name() # Get joystick system name
print logitech_joystick.get_numaxes() # Get number of axes on joystick
print logitech_joystick.get_numballs() # Get number of track balls
print logitech_joystick.get_numbuttons() # Get number of buttons on the joystick
print logitech_joystick.get_numhats() # Get number of hat controls


while True: # Loop forever
    pygame.event.pump() # Process pygame event handlers
    positionX = logitech_joystick.get_axis(0)
    positionY = logitech_joystick.get_axis(1)
    positionZ = logitech_joystick.get_axis(2)
    currentButton = logitech_joystick.get_button(6)
    button8 = logitech_joystick.get_button(7)
    button9 = logitech_joystick.get_button(8)
    button10 = logitech_joystick.get_button(9)
    button11 = logitech_joystick.get_button(10)

    time.sleep(0.1)

    print positionX # Get current position of an axis
    print positionY
    print positionZ
    #print currentButton
    #print button8, button9, button10, button11

