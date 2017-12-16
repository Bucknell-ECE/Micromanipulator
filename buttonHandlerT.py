import pygame
import time


pygame.init()


done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

button2count = 0
# -------- Main Program Loop -----------
while done == False:
    # EVENT PROCESSING STEP
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            #print("Joystick button pressed.")
            print(event)
        if event.type == pygame.JOYBUTTONUP:
            #print("Joystick button released.")
            print(event)
            #print(event.type)
            #print(event.button)
            button = event.button
            print("Button {} off".format(button))
            if button == 2:
                button2count += 1
        print('Button 2 Coutnt is : ', button2count)

    time.sleep(2)

    # Limit to 20 frames per second
    clock.tick(20)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()