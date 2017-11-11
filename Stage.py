import smbus
from helper import *
class Stage:

    def __init__(self, address, position, bus):
        self.position = position
        self.address = address
        self.bus = smbus.SMBus(bus)
    bus = smbus.SMBus(1)
   # def getPosFromM3LS(self):

    def getPosition(self):
        return int(self.position)
    def getAddress(self):
        return self.address

    def buildCommand(self, commandCode, commandVars):
        """
        Function that builds a command that is ready to be sent to a stage. The command is output in a list that is
        comprised of the hexadecimal values
        """

        command = []  # empty list to hold command
        command += [self.address << 1]  # address of stage bit shifted 1 left
        command += [60]  # open carat(<)
        for i in str(commandCode):
            command += [ord(i)]
        command += [32]  # space(' ')
        command += commandVars
        command += [62]  # close carat (>)
        command += [13]  # carriage return(\r)
        return command

    def buildCommandNoVars(self, commandCode):
        """
        Function that builds a command that is ready to be sent to a stage. The command is output in a list that is
        comprised of the hexadecimal values
        """
        command = []
        command += [self.address << 1]
        command += [60]
        for i in str(commandCode):
            command += [ord(i)]
        command += [62]
        command += [13]
        return command


    def write(self, command):
        bus = smbus.SMBus(1)
        bus.write_i2c_block_data(self.address, 0, command)

    def sendCommand(self, commandCode, commandVars):
        commandToSend = self.buildCommand(commandCode, commandVars)
        self.write(commandToSend)


    def sendCommandNoVars(self, commandCode):
        commandToSend = self.buildCommandNoVars(commandCode)
        print('commant no vars: ', commandToSend)
        self.write(commandToSend)


    def calibrate(self):
        self.sendCommand('87', [' 5'])

    def startup(self):
        #forwardStep = ['0x31', '0x20', '0x30', '0x30', '0x30', '0x30', '0x30', '0x30', '0x36', '0x34']
        ##backwardStep =
        self.sendCommand('06', ['0x31'] + ['0x20'] + encoderConvert(64))

    def getPositionFromM3LS(self):
        """
        Function that returns the position of the stage
        :return: Postion of the stage in encoder counts(NOT uM!)

        From newscale documentation:
        Send : <10>
        Receive: <10 SSSSSS PPPPPPPP EEEEEEEE>
        S is motor status
        P is position, hex representation of encoder counts
        E is error count. How far is the stage from where it is supposed to be?
        """
        bus = self.bus
        self.sendCommandNoVars('10')  #send query asking about motor status and position
        temp = bus.read_i2c_block_data(0x32, 0)  #store incoming data from motor in list

        rcvEncodedPosition = ''
        for element in range(8):
            rcvEncodedPosition += str(chr(temp[11+element]))
        position = int(rcvEncodedPosition, 16)
        return position


