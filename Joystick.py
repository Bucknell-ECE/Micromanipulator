import pygame
#from helper import mapval

def mapval(x, inMin, inMax, outMin, outMax):
    """
    Maps a value in one range to a value in another range
    :param x: value to be mapped
    :param inMin: minimum of the input scale
    :param inMax: maximum of the input scale
    :param outMin: minimum of the output scale
    :param outMax: maximum of the output scale
    :return: mapped value, rounded to the nearest integer value
    """
    return int(round((x - inMin) * (outMax - outMin) / (inMax - inMin) + outMin, 0))

xAxisNum = 0
yAxisNum = 1
throttleAxisNum = 2
buttonMap = {
    1: 'Zdown',
    2: 'Zup',
    3: 'Hold',
    4: 'ChangeMode',
}

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


############################CODE WRITTTEN BY RYDER#########################################
    def getButtons(self):
        clock = pygame.time.Clock()

        commands = []

        for event in pygame.event.get():  # User did something
            #print(event)
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop

            # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
            if event.type == pygame.JOYBUTTONDOWN:
                button = event.button
                #commands += button
                commands += [buttonMap[button]]
            clock.tick(20)

        return commands


    def getAbsoluteX(self):
        pygame.event.get()
        #joystick = pygame.joystick.Joystick(0)
        return self.joystick.get_axis(xAxisNum)

    def getAbsoluteY(self):
        pygame.event.get()
        #joystick = pygame.joystick.Joystick(0)
        return self.joystick.get_axis(yAxisNum)

    def getAbsoluteThrottle(self):
        pygame.event.get()
        #joystick = pygame.joystick.Joystick(0)
        return self.joystick.get_axis(throttleAxisNum)

    def getAbsolutePosition(self):
        pygame.event.get()
        position = [round(self.joystick.get_axis(xAxisNum), 3), round(self.joystick.get_axis(yAxisNum), 3)]
        return position

    def getX(self):
        pygame.event.get()
        #joystick = pygame.joystick.Joystick(0)
        absoluteX = self.getAbsoluteX() + 1
        return mapval(absoluteX, 0, 2, 0, 1023)

    def getY(self):
        pygame.event.get()
        #joystick = pygame.joystick.Joystick(0)
        absoluteY = self.getAbsoluteY() + 1
        return mapval(absoluteY, 0, 2, 0, 1023)

    def getThrottle(self):
        pygame.event.get()
        #joystick = pygame.joystick.Joystick(0)
        absoluteThrottle = self.getAbsoluteThrottle()
        return mapval(absoluteThrottle, -1, 1, 0, 100)

    def getPosition(self):
        pygame.event.get()
        #position = [round(self.joystick.get_axis(xAxisNum), 3), round(self.joystick.get_axis(yAxisNum), 3)]
        absolutePosition = [self.getAbsoluteX() + 1, self.getAbsoluteY() + 1]
        return map(lambda x: mapval(x, 0, 2, 0, 1023), absolutePosition)
