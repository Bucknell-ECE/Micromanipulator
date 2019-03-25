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

        axis = spidev.SpiDev()
        axis.open(self.bus, self.device)
        axis.mode = 0b01
        axis.max_speed_hz = 1000000  # Change to 62.5 MHz (test) from 1 MHz (TEST)
        self.axis = axis


    def write(self, command):
        """
        Function to write to the SPI Stages.
        :param command: Command in the form of a list of decimal integers, each of which represents an ascii character
        in the command to be sent to the stage.
        :return: NA
        """
        print(command_to_string(command))  # print the command in a user readable format
        self.axis.writebytes(command)  # 'writebytes(foo)' is an SpiDev() command


    def read(self):
        """
        Reads from the output register of the stage
        :return: List of signed values that represent what is on the output register of the stage
        """
        temp = self.axis.readbytes(EXPECTED_RETURN_LENGTH)  # SpiDev() command
        print('temp', temp)
        return_buffer = []
        for i in temp:
            return_buffer += str(chr(int(i)))
        print(return_buffer)
        return return_buffer


    def get_status(self):
        """Get current status information
        return a series of bits that correspond to the table on the reference manual <10>
        """
        self.send_command_no_vars('10')
        time.sleep(0.2)  # TODO Magic number! Try playing around with this.
        temp = self.read()
        #return temp

        rcv_encoded_status = ''
        for element in range(6):
            rcv_encoded_status += str(temp[6 + element])
        print(rcv_encoded_status)

        status = ''
        for element in range(len(rcv_encoded_status)):
            #binary_string = binascii.unhexlify(rcv_encoded_status[element])
            #status += binary_string
            binary_string = format(int(rcv_encoded_status[element]),'04b')
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