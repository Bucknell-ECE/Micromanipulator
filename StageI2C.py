import Stage
import smbus
import time
from Stage import Stage
class StageI2C(Stage):
    def __init__(self, address, position, bus):
        Stage.__init__(self, position)
        self.position = position
        self.address = address
        self.bus = smbus.SMBus(bus)
        self.home = 6000

    bus = smbus.SMBus(1)


    def zMove(self, direction, encoderCounts):
        """

        :param direction: The direction for Z to move. 1= up 0 = down
        :param encoderCounts: number of encoder counts to move
        :return: NA

        """
        command = '06 ' + str(direction)
        self.sendCommand(command, encodeToCommand(encoderCounts))


    def write(self, command):
        bus = smbus.SMBus(1)
        #bus.write_i2c_block_data(self.address, 0, command)
        ##############CHANGED TO 1 BUT SHOULD BE ZERO

        print(commandToString(command))  # print the command in  a user readable format.

        bus.write_i2c_block_data(self.address, 0, command)

    def write1(self, command):
        bus = smbus.SMBus(1)
        #bus.write_i2c_block_data(self.address, 0, command)
        bus.write_i2c_block_data(0x32, 0, command)

    def read(self):
        """
        Reads from the output register of the stage
        :return: List of signed values that reprsent what is on the output register of the stage
        """
        bus = self.bus
        temp = bus.read_i2c_block_data(self.address, 0)
        print('temp', temp)
        returnBuffer = []
        for i in temp:
            returnBuffer += str(chr(int(i)))

        return returnBuffer

