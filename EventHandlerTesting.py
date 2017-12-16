import pygame
import time

# Define some colors
#BLACK = (0, 0, 0)
#WHITE = (255, 255, 255)


# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputting the
# information.
'''
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def printy(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10

'''
pygame.init()

# Set the width and height of the screen [width,height]
#size = [500, 700]
#screen = pygame.display.set_mode(size)

#pygame.display.set_caption("My Game")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()
# Get ready to print
#textPrint = TextPrint()
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


    # DRAWING STEP
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    #screen.fill(WHITE)
    #textPrint.reset()

    # Get count of joysticks
#    joystick_count = pygame.joystick.get_count()

    # For each joystick:
#    for i in range(joystick_count):
 #       joystick = pygame.joystick.Joystick(i)
 #       joystick.init()



        # Get the name from the OS for the controller/joystick






    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

    # Go ahead and update the screen with what we've drawn.
    #pygame.display.flip()

    # Limit to 20 frames per second
    clock.tick(20)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()