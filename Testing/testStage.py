## Current unused (7/5/18)

from helper import *
from Stage import *

x_axis = Stage(0x33, 6000, 1)
print(x_axis.address)
print(x_axis.get_address())
print(2 * x_axis.get_address())
while True:
    bus = smbus.SMBus(1)
    next = input('What do you want to do next?')
    #1. Read Status register
    #2. move to a location
    #3. get full status
    #4. read firmware version
    #5. get current position
    #6. calibrate
    #7. set home position
    #8. go home
    if next == 1: # read status register
        temp = bus.read_i2c_block_data(0x33, 19)
        print('temp', temp)
    elif next == 2: #move to a location
        moveToNew = input('Where should the stage move next?')
        # com = x_axis.build_command('08',encoder_convert(moveToNew))
        # print(com)
        # x_axis.calibrate()
        # bus.write_i2c_block_data(0x32, 0, [100, 60, 48, 56, 32, 48, 48, 48, 48, 48, 51, 69, 56, 62, 13])
        x_axis.send_command('08', encoderCountConvert(moveToNew))
    elif next == 3: #get full status
        x_axis.send_command_no_vars('19')
        temp = bus.read_i2c_block_data(0x33, 0)
        print('temp', temp)
    elif next == 4:# read firmware version
        x_axis.send_command_no_vars('01')
        temp = bus.read_i2c_block_data(0x33, 0)
        print('temp', temp)
    elif next == 5: #get current postion
        pos = x_axis.get_position_from_M3LS()
        print(pos)
    elif next == 6: #calibrate
        x_axis.calibrate()
        temp = bus.read_i2c_block_data(0x33, 0)
        print('temp', temp)
    elif next == 8: #Return home
        x_axis.return_home()
    elif next == 7:
        newHome = input('Enter -1 to set current location as home, or enter postiion to set home')
        if newHome == -1:
            x_axis.set_current_home()
        else:
            x_axis.set_home(newHome)







