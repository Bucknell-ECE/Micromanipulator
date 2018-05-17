import pygame
from Joystick import CustomJoystick
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputting the
# information.
class Console:
    def __init__(self):
        pygame.init()


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


pygame.init()
# Set the width and height of the screen [width,height]
size = [500, 700]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# # Initialize the joysticks
# pygame.joystick.init()



    #This is the method that shouls be used in the future, where a joystick and stage object are passes to the function
    #and it does everthing that way
    # def displayUpdates(self, CustomJoystick):
    #     x = CustomJoystick.getX()

def displayUpdates(self, scaled_range, x_linear_range_min, x_linear_range_max, y_linear_range__min,
                   y_linear_range_max, axes, x_joy, y_joy):
    # Get ready to print
    global screen
    global clock
    global size
    textPrint = TextPrint()
    # size = [500, 700]
    # clock = pygame.time.Clock()
    # screen = pygame.display.set_mode(size)
    screen.fill(WHITE)
    textPrint.reset()
    for i in range(len(axes)):
        ax_labels = ['X', 'Y', 'Z']
        textPrint.printy(screen, "Axis {} value: {:>6.3f}".format(ax_labels[i], axes[i]))
    textPrint.unindent()

    textPrint.printy(screen,"Scaled Range is : {:>6.3f}".format(scaled_range))


    pygame.display.flip()

    # Limit to 20 frames per second
   # clock.tick(20)


