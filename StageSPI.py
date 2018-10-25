'''
This file contains the stage functions for the x and y axis communicating via SPI. DO NOT USE THIS FOR COMMUNICATING

WITH I2C Stages. It will fail. This only contains the Overide methods for the SPI stuff.


Last Modified: R. Nance 5/15/2018
#####################DO NOT EDIT BELOW INFORMATION##################################
Originating Branch: Master
Originally Created: R. Nance 05/2018
'''

from Stage import Stage
from helper import *

import time
import spidev
import binascii

EXPECTED_RETURN_LENGTH = 31  # TODO Message from stage is expected to be 31 bytes long (verify in C&C Ref. Guide)


class StageSPI(Stage):
    def __init__(self, bus, device, position):
        Stage.__init__(self, position)  # StageSPI is a child class of Stage -- inherits everything from Stage

        self.position = position
        self.bus = bus
        self.device = device
        self.home = 6000

        #self.axis = axis
        #stageAxis = axis
        #axis = spidev.SpiDev()
        #axis.open(bus, device)
        #axis.mode = 0b01
        #axis.max_speed_hz = 1000000

        # TODO figure out the differences between these two

        axis = spidev.SpiDev()
        axis.open(self.bus, self.device)
        axis.mode = 0b01
        axis.max_speed_hz = 1000000  # TODO Responsiveness of 1 MHz? (Is this used anywhere?)
        self.axis = axis


    def write(self, command):
        """
        Function to write to the SPI Stages.
        :param command: Command in the form of a list of decimal integers, each of which represents an ascii character
        in the command to be sent to the stage.
        :return: NA
        """
        print(commandToString(command))  # print the command in a user readable format
        self.axis.writebytes(command)

    def read(self):
        """
        Reads from the output register of the stage
        :return: List of signed values that represent what is on the output register of the stage
        """
        temp = self.axis.readbytes(EXPECTED_RETURN_LENGTH)
        print('temp', temp)
        return_buffer = []
        for i in temp:
            return_buffer += str(chr(int(i)))
        print(return_buffer)
        return return_buffer

    def getstatus(self):
        """Get current status information
        return a series of bits that correspond to the table on the reference manual <10>
        """
        self.sendCommandNoVars('10')
        time.sleep(0.2)  # TODO Magic number! Try playing around with this.
        temp = self.read()
        #return temp

        rcvEncodedStatus = ''
        for element in range(6):
            rcvEncodedStatus += str(temp[6 + element])
        print(rcvEncodedStatus)

        status = ''
        for element in range(len(rcvEncodedStatus)):
            #binary_string = binascii.unhexlify(rcvEncodedStatus[element])
            #status += binary_string
            binary_string = format(int(rcvEncodedStatus[element]),'04b')
            status += binary_string

        return status


    # def MotorDirection(self, status):
    #     if status[1] == '0':
    #         print('Running Reverse')
    #     else:
    #         print('Running Forward')
    #
    # def Running(self, status):
    #     if status[1] == '0':
    #         print('Motor is not running')
    #     else:
    #         print('Motor is running')