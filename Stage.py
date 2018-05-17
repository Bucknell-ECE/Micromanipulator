'''
This file contains the stage functions for I2C Communication ONLY!! THIS IS NOT TO BE USED FOR SPI COMMUNICATION. This
is for the Z axis.
Last Modified: R. Nance 5/15/2018
#####################DO NOT EDIT BELOW INFORMATION##################################
Originating Branch: Master
Originally Created: R. Nance 12/2017
'''
from helper import *
import time

class Stage:

    def __init__(self, position):
        self.position = position
        self.home = 6000


    def getPosition(self):
        return int(self.position)

    def getAddress(self):
        return self.address

    def setHome(self, location):
        """
        Allows user to set the home location for the particular axis
        :param location: a location, specified in encoder counts
        :return: NA
        """
        self.home = location
    def setCurrentHome(self):
        current = self.getPositionFromM3LS()
        self.setHome(current)

    def buildCommand(self, commandCode, commandVars):
        """
        Function that builds a command that is ready to be sent to a stage. The command is output in a list that is
        comprised of the hexadecimal values
        """
        command = []  # empty list to hold command
        # command += [self.address << 1]  # address of stage bit shifted 1 left
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

        command += [60]  # '<'
        for i in str(commandCode):
            command += [ord(i)]
        command += [62]  # '>'
        command += [13]  # '\r'

        return command

    def sendCommand(self, commandCode, commandVars):
        commandToSend = self.buildCommand(commandCode, commandVars)

        print(commandToString(commandToSend))

        self.write(commandToSend)

    def sendCommandNoVars(self, commandCode):
        commandToSend = self.buildCommandNoVars(commandCode)
        #print('command no vars: ', commandToSend)
        self.write(commandToSend)

    def calibrate(self):
        """
        Function that runs a calibration for the stages. Runs both forward and backwards commands.
        :return: N/A
        """
        '''
        Send to stage:
        <87 5>/r
        Recieve from stage:

        '''
        self.sendCommand('87', [ 5])
        time.sleep(0.2)
        self.sendCommand('87', [ 4])
        time.sleep(0.2)

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

        self.sendCommandNoVars('10')  # send query asking about motor status and position
        time.sleep(0.2)
        temp = self.read()  # store incoming data from motor in list

        rcvEncodedPosition = ''
        for element in range(8):
            #print(temp[6])
            #print(13 + element)
            #print(temp[int(13 + element)])
            #print(chr(temp[11 + element]))
            rcvEncodedPosition += str(temp[13 + element])
        #print(rcvEncodedPosition)
        position = int(rcvEncodedPosition, 16)
        print('The current position Reported by M3LS is : ', position)
        return position
    def goToLocation(self, location):
        """
        Sends the stage to the location specified, in encoder counts
        :param location: a location in encoder counts
        :return: NA
        """
        #print(encodeToCommand(location)) ###FOR DEBUGGING PURPOSES######
        self.sendCommand('08', encodeToCommand(location))

    def returnHome(self):
        """
        Funtion that sends the stage to its home location
        :return: NA
        """
        self.goToLocation(self.home)




#########################DEPRECATED CODE#########################

    # def write1(self, command):
    #     bus = smbus.SMBus(1)
    #     #bus.write_i2c_block_data(self.address, 0, command)
    #     bus.write_i2c_block_data(0x32, 0, command)





