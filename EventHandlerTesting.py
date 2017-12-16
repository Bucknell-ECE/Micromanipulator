import pygame


pygame.init() # Initialize all pygame modules
pygame.joystick.init() # Initialize joystick module
size = [500, 700]
screen = pygame.display.set_mode(size)

while True:
    for event in pygame.event.get():  # User did something

        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")