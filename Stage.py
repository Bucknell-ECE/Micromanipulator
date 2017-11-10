import smbus
from helper import *
class Stage:

    def __init__(self, address, position, bus):
        self.position = position
        self.address = address
        self.bus = bus
    bus = smbus.SMBus(1)
   # def getPosFromM3LS(self):

    def getPosition(self):
        return int(self.position)
    def getAddress(self):
        return self.address

    def buildCommand(self, commandCode, commandVars):
        ''''
        Function that builds a command that is ready to be sent to a stage. The command is output in a list that is
        comprised of the hexadecimal values
        '''

        command = [] #empty list to hold command
        command += [int(self.address[2:]) << 1]  # address of stage bit shifted 1 left
        command += [60] # open carat
        for i in str(commandCode):
            command += [ord(i)]
        command += [32] # space
        command += commandVars
        command += [62] # close carat
        command += [13] # carriage return
        print(command)
        print([command[1] + command[2]])
        return command

    def buildCommandNoVars(self, commandCode):
        ''''
        Function that builds a command that is ready to be sent to a stage. The command is output in a list that is
        comprised of the hexadecimal values
        '''

        command = []
        command += ['0x' + str(int(self.address[2:]) << 1)]
        command += ['0x3C']
        for i in str(commandCode):
            command += [hex(ord(i))]
        command += ['0x3E']
        command += ['0x0D']
        return command


    def write(self, command):
        print(command)
        print(command[1] + command[2])
        bus = smbus.SMBus(1)
        print('found bus')
        bus.write_i2c_block_data(self.address, 0, command)
    def sendCommand(self, commandCode, commandVars):
        print('Command code', commandCode, 2 * commandCode)
        print('command vars', commandVars, commandVars[1]+commandVars[2])
        commandToSend = self.buildCommand(commandCode, commandVars)
        print('commmand to sent', commandToSend)
        print('added' , commandToSend[1] + commandToSend[2])
        self.write(commandToSend)
        print('written')

    def sendCommandNoVars(self, commandCode):
        commandToSend = self.buildCommandNoVars(commandCode)
        self.write(commandToSend)

    def calibrate(self):
        self.sendCommand('87', ['0x35'])

    def startup(self):
        #forwardStep = ['0x31', '0x20', '0x30', '0x30', '0x30', '0x30', '0x30', '0x30', '0x36', '0x34']
        ##backwardStep =
        self.sendCommand('06', ['0x31'] + ['0x20'] + encoderConvert(64))
    """
    def getPositionFromM3LS(self):
        self.sendCommandNoVars(19)
        temp =[]
        temp = bus.read_i2c_block_data(32, charcmd)
    """
