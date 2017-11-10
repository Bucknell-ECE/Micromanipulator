from helper import *
from Stage import *

xaxis = Stage('0x32', 6000, 1)

while True:
    bus = smbus.SMBus(1)

    moveToNew = input('Where should the stage move next?')
    #com = xaxis.buildCommand('08',encoderConvert(moveToNew))
    #print(com)
    #xaxis.calibrate()
    bus.write_i2c_block_data(0x32, 0, [64,60,48,56,32,30,30,30,30,30,66,66,56,62,13])
    #xaxis.sendCommand('08', encoderCountConvert(moveToNew))
    input('Finished, Continue?')


