from helper import *
from Stage import *
xaxis = Stage(0x32, 6000, 1)
yaxis = Stage(0x33, 6000, 1)
zaxis = Stage(0x34, 6000, 1)
controlMode = 'velocity'
xlinearRangeMin = 0
xlinearRangeMax = 12000
xlinearRange = 12000
ylinearRangeMin = 0
ylinearRangeMax = 12000
ylinearRange = 12000
axes = [xaxis, yaxis, zaxis]
home = [xaxis.home, yaxis.home, zaxis.home]
def setControlMode(newControlMode):
    controlMode = newControlMode


while True:
    if controlMode == 'velocity':
        fsdjfl
    if controlMode == 'position':
        xaxis.goToLocation(mapval(home[i], 0, 255, xlinearRangeMin, xlinearRangeMax))
        yaxis.goToLocation(mapval(home[i], 0, 255, xlinearRangeMin, xlinearRangeMax))

        joyx = 1
        joyy = 1


def setBounds():
    """
    Sets the bounds for position mode.
    :return: na
    """
    global xlinearRangeMin
    global xlinearRangeMax
    global ylinearRangeMin
    global ylinearRangeMax
    xlinearRangeMin = xaxis.home - xlinearRange
    xlinearRangeMax = xaxis.home + xlinearRange
    ylinearRangeMin = yaxis.home - ylinearRange
    ylinearRangeMax = yaxis.home + ylinearRange
