from helper import *
from Stage import *

xaxis = Stage('0x32', 6000, 1)

while True:
    moveToNew = input('Where should the stage move next?')
    #com = xaxis.buildCommand('08',encoderConvert(moveToNew))
    #print(com)
    #xaxis.calibrate()
    xaxis.sendCommand('08', encoderConvert(moveToNew))
    input('Finished, Continue?')


