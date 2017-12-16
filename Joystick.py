import pygame
from helper import mapval


xAxisNum = 0
yAxisNum = 1
throttleAxisNum = 2
class CustomJoystick:
    #will need to create a button mapping function that imports text file stuff here.
    def __init__(self, name):
        self.name = name
        self.numberaxes = numberaxes
        self.numberbuttons = numberbuttons

        joystick_count = pygame.joystick.get_count()
        joystick = pygame.joystick.Joystick(i)
        # For each joystick:
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()

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
        joystick = pygame.joystick.Joystick(0)
        return joystick.get_axis(xAxisNum)

    def getY(self):
        joystick = pygame.joystick.Joystick(0)
        return joystick.get_axis(yAxisNum)

    def getThrottle(self):
        joystick = pygame.joystick.Joystick(0)
        return joystick.get_axis(throttleAxisNum)