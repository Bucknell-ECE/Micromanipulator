import Stage
import smbus
import time
from Stage import Stage
from helper import *


class StageI2C(Stage):
    def __init__(self, address, position, bus):
        Stage.__init__(self, position)
        self.position = position
        self.address = address
        self.bus = smbus.SMBus(bus)
        self.home = 6000
    bus = smbus.SMBus(1)  # initialize the SMBus (I2C bus) on the pi. The bus we use is 1.

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
        :param command: The compiled command to be send to the stages. This should be a list of the
        decimal values for each of the ascii characters in the command to be sent.
        :return:
        """
        bus = smbus.SMBus(1)
        print(commandToString(command))  # print the command in  a user readable format.
        bus.write_i2c_block_data(self.address, 0, command)

    def read(self):
        """
        Reads from the output register of the stage
        :return: List of signed values that reprsent what is on the output register of the stage
        """
        bus = self.bus
        temp = bus.read_i2c_block_data(self.address, 0)
        print('temp', temp)
        return_buffer = []
        for i in temp:
            return_buffer += str(chr(int(i)))

        return return_buffer

