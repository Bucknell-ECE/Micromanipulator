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


class Stage(object):

    def __init__(self, position):

        self.position = position
        self.home = 6000

    #  @property
    def getPosition(self):
        return int(self.position)

    # @property
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
        print('The current home for this axis is now', current)
        self.setHome(current)
        print('The self.home home is now ', self.home)

    def buildCommand(self, command_code, command_vars):
        """
        Function that builds a command that is ready to be sent to a stage. The command is output in a list that is

        comprised of the decimal(##CHANGE TO HEX?##)  values of each ASCII character in the command code, the optional
        parameters, and the

        carriage return (\r)
        :param command_code: two digit integer for the command you want to send. For example: Move to target is 08
        :param command_vars: the optional parameter for the command, in list form.
        :return:
        """
        command = []  # empty list to hold command
        # command += [self.address << 1]  # address of stage bit shifted 1 left
        command += [60]  # open carat(<)
        for i in str(command_code):
            command += [ord(i)]
        command += [32]  # space(' ')
        command += command_vars
        command += [62]  # close carat (>)
        command += [13]  # carriage return(\r)
        return command

    def buildCommandNoVars(self, command_code):
        """
        Function that builds a command that is ready to be sent to a stage. The command is output in a list that is

        comprised of the decimal(##CHANGE TO HEX?##) values of each ASCII character in the command + the carriage
        return (\r)


        :param command_code: two digit integer for the command you want to send. For example: Move to target is 08
        :return: The command, in the form of a list of integer values each of which represents an ascii character in
        the command that you want to send.
        """
        command = []

        command += [60]  # '<'
        for i in str(command_code):

            command += [ord(i)]
        command += [62]  # '>'
        command += [13]  # '\r'

        return command

      
    def sendCommand(self, command_code, command_vars):
        """
        Sends a command that has both a code and optional parameters. Optional parameters are listed in the newscale
        documentation in square brackets.
        :param command_code: two digit integer for the command you want to send. For example: Move to target is 08........
        :param command_vars: the optional paramter for the command, in list form.
        :return:
        """
        command_to_send = self.buildCommand(command_code, command_vars)
        #return command_to_send
        #return(commandToString(command_to_send))
        #print(commandToString(command_to_send))
        self.write(command_to_send)


    def sendCommandNoVars(self, command_code):
        """
        Sends a command that does not have optional paramters.
        :param command_code: two digit integer for the command you want to send. For example: Move to target is 08
        :return:
        """
        command_to_send = self.buildCommandNoVars(command_code)
        #print(commandToString(command_to_send))
        self.write(command_to_send)

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
        """
        Runs the Newscale recommended startup sequence. This is not yet complete. See Newscale docs page 7
        :return: NA
        """
        #forwardStep = ['0x31', '0x20', '0x30', '0x30', '0x30', '0x30', '0x30', '0x30', '0x36', '0x34']
        ##backwardStep =
        #self.sendCommand('06', ['0x31'] + ['0x20'] + encoderConvert(64))
        self.sendCommand('06', [48] + [32] + encodeToCommand(100))
        self.sendCommand('06', [49] + [32] + encodeToCommand(100))
        #self.calibrate()

    def getPositionFromM3LS(self):
        """
        Function that returns the position of the stage
        :return: Position of the stage in encoder counts(NOT uM!)

        From Newscale documentation:
        Send : <10>
        Receive: <10 SSSSSS PPPPPPPP EEEEEEEE>
        S is motor status
        P is position, hex representation of encoder counts
        E is error count. How far is the stage from where it is supposed to be?
        """

        self.sendCommandNoVars('10')  # send query asking about motor status and position
        time.sleep(0.2)
        temp = self.read()  # store incoming data from motor in list
        print ('This is temp',temp)

        rcvEncodedPosition = ''
        for element in range(8):
            rcvEncodedPosition += str(temp[13 + element])
        position = int(rcvEncodedPosition, 16)
        print('The current position Reported by M3LS is : ', position)
        return position

    def GetCloseLoopSpeed(self):
        self.sendCommandNoVars('40')
        time.sleep(0.2)
        temp = self.read()
        print('This is speed',temp)




    def goToLocation(self, location):
        """
        Sends the stage to the location specified, in encoder counts
        :param location: a location in encoder counts
        :return: NA
        """

        #print(encodeToCommand(location)) ###FOR DEBUGGING PURPOSES######

        self.sendCommand('08', encodeToCommand(location))

    def movesteps(self,steps):

        self.sendCommand('06',[48] + [32] + encodeToCommand(steps))

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




#########################DEPRECATED CODE#########################

    # def write1(self, command):
    #     bus = smbus.SMBus(1)
    #     #bus.write_i2c_block_data(self.address, 0, command)
    #     bus.write_i2c_block_data(0x32, 0, command)





