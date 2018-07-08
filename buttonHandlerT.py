## unused (7/5/18)

import pygame
import time

pygame.init()

# Initialize the joysticks
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

button2count = 0
# -------- Main Program Loop -----------


while True:
    # EVENT PROCESSING STEP
    test = input('Type a key when you would like a status update')
    if test == 1:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.JOYBUTTONUP:
                button = event.button
                print("Button {} off".format(button))
                #if button == 2:
                   # button2count += 1
            #print('Button 2 Coutnt is : ', button2count)

        #time.sleep(2)

#pygame.quit()