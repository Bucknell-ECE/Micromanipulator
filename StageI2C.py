'''
This file contains the the submethods for the I2C Stages.
Last Modified: R. Nance 5/15/2018
#####################DO NOT EDIT BELOW INFORMATION##################################
Originating Branch: MergeStageClasses
Originally Created: R. Nance 12/2017
'''
import Stage
import smbus
import time
import binascii
from Stage import Stage
from helper import *


class StageI2C(Stage):
    def __init__(self, address, position, bus):
        Stage.__init__(self, position)
        self.position = position
        self.address = address
        self.bus = smbus.SMBus(bus)  # Initialize the SMBus(I2C, lookup the differences)
        self.home = 6000

    def zMove(self, direction, encoder_counts):
        """
        :param direction: The direction for Z to move. 1= up 0 = down
        :param encoder_counts: number of encoder counts to move
        :return: NA
        """
        command = '06 ' + str(direction)
        self.sendCommand(command, encodeToCommand(encoder_counts))

    def write(self, command):
        """
        The command to write to the stages in I2C.
        :param command: Command in the form of a list of decimal integers, each of which represents an ascii character
        in the command to be sent to the stage.
        :return:
        """
        print(commandToString(command))  # print the command in  a user readable format.
        self.bus.write_i2c_block_data(self.address, 0, command)

    def read(self):
        """
        Reads from the output register of the stage. I think that there may be a limit to the number of bits that can
        be read back but I am not entirely sure. This should be checked.
        :return: List of signed values that represent what is on the output register of the stage
        """
        temp = self.bus.read_i2c_block_data(self.address, 0)
        print('temp', temp)
        return_buffer = []
        for i in temp:
            return_buffer += str(chr(int(i)))

        return return_buffer

    def getstatus(self):
        self.sendCommandNoVars('10')  # send query asking about motor status and position
        time.sleep(0.2)
        temp = self.read()  # store incoming data from motor in list
        #return temp

        rcvEncodedStatus = ''
        for element in range(6):
            rcvEncodedStatus += str(temp[4 + element])
        #return rcvEncodedStatus

        status = ''
        for element in range(len(rcvEncodedStatus)):
            # binary_string = binascii.unhexlify(rcvEncodedStatus[element])
            # status += binary_string
            binary_string = format(int(rcvEncodedStatus[element]),'04b')
            print(binary_string)

        # return status
