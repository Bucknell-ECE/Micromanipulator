import pygame
#from helper import mapval


xAxisNum = 0
yAxisNum = 1
throttleAxisNum = 2
class CustomJoystick:
    #will need to create a button mapping function that imports text file stuff here.
    def __init__(self, name, number):
        self.name = name
        self.joystick = pygame.joystick.Joystick(number)
        pygame.init()



        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()

        # Initialize the joysticks
        pygame.joystick.init()


        joystick_count = pygame.joystick.get_count()
        joystick = pygame.joystick.Joystick(0)


        # For each joystick:
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            #print('this is joystick: ', i)
            joystick.init()
        axes = joystick.get_numaxes()
        #print(axes)
    def getAxisPosition(self, axisIndex):
        joystick = pygame.joystick.Joystick(0)
        return joystick.get_axis(axisIndex)

    def convertPosition(self, axisIndex):
        currPos = self.getAxisPosition(axisIndex)
        newPos = (currPos + 1)*127.5
        return newPos
    #def getButtons(self):
       # fdshkj

    def getX(self):
        pygame.event.get()
        #joystick = pygame.joystick.Joystick(0)
        return self.joystick.get_axis(xAxisNum)

    def getY(self):
        pygame.event.get()
        #joystick = pygame.joystick.Joystick(0)
        return self.joystick.get_axis(yAxisNum)

    def getThrottle(self):
        pygame.event.get()
        #joystick = pygame.joystick.Joystick(0)
        return self.joystick.get_axis(throttleAxisNum)

    def getPosition(self):
        pygame.event.get()
        position = [self.joystick.get_axis(xAxisNum), self.self.joystick.get_axis(yAxisNum)]
        return position