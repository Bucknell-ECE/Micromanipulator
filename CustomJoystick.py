import pygame

class CustomJoystick:

    def __init__(self, name, numberaxes, numberbuttons):
        self.name = name
        self.numberaxes = numberaxes
        self.numberbuttons = numberbuttons

    def getAxisPosition(self, axisIndex):
        return self.get_axis(axisIndex)

    def convertPosition(self, axisIndex):
        currPos = self.getAxisPosition(self, axisIndex)
        newPos = (currPos + 1)*127.5
        return newPos
