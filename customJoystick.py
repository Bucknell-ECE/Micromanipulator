import pygame

class CustomJoystick:

    def _init_(self, type, numberaxes, numberbuttons):
        self.type = type
        self.numberaxes = numberaxes
        self.numberbuttons = numberbuttons

    def getAxisPosition(self, axisIndex):
        return self.get_axis(axisIndex)

    def convertPosition(self, axisIndex):
        currPos = self.getAxisPosition(self, axisIndex)
        newPos = (currPos + 1)*127.5
        return newPos
