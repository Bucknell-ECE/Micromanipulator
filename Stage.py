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

        # self.startup()  # TODO Uncomment this to run startup sequence.
        self.position = position    # initialize position parameter
        self.home = 6000            # move stage to 6000 (encoder cts) at startup


     # @property TODO What does @property do, and should I use it?
    def get_position(self):
        return int(self.position)  # TODO Do we need to rename this function?


    # @property
    def get_address(self):
        return self.address


    def set_home(self, location):
        """
        Allows user to set the home location for the particular axis
        :param location: a location, specified in encoder counts
        :return: NA
        """
        self.home = location


    def set_current_home(self):
        current = self.get_position_from_M3LS()

        print('The current home for this axis is now', current)
        self.set_home(current)
        print('The self.home home is now ', self.home)


    def get_position_from_M3LS(self):
        """
        Function that returns the position of the stage
        :return: Position of the stage in encoder counts (NOT uM!)

        From Newscale documentation:
        Send : <10>
        Receive: <10 SSSSSS PPPPPPPP EEEEEEEE>
        S is motor status
        P is position, hex representation of encoder counts
        E is error count. How far is the stage from where it is supposed to be?
        """

        self.send_command_no_vars('10')  # send query asking about motor status and position
        time.sleep(0.2)     ## TODO What is the purpose of this delay?
        temp = self.read()  # store incoming data from motor in list
        print ('This is temp',temp)

        rcv_encoded_position = ''

        for element in range(8):
            rcv_encoded_position += str(temp[13 + element])

        position = int(rcv_encoded_position, 16)

        print('The current position Reported by M3LS is : ', position)
        return position


    def build_command(self, command_code, command_vars):
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


    def build_command_no_vars(self, command_code):
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


    def send_command(self, command_code, command_vars):
        """
        Sends a command that has both a code and optional parameters. Optional parameters are listed in the newscale
        documentation in square brackets.
        :param command_code: two digit integer for the command you want to send. For example: Move to target is 08........
        :param command_vars: the optional paramter for the command, in list form.
        :return:
        """
        command_to_send = self.build_command(command_code, command_vars)
        #return command_to_send
        #return(command_to_string(command_to_send))
        #print(command_to_string(command_to_send))
        self.write(command_to_send)


    def send_command_no_vars(self, command_code):
        """
        Sends a command that does not have optional paramters.
        :param command_code: two digit integer for the command you want to send. For example: Move to target is 08
        :return:
        """
        command_to_send = self.build_command_no_vars(command_code)
        #print(command_to_string(command_to_send))
        self.write(command_to_send)


    def calibrate(self):
        """
        Function that runs a calibration for the stages. Runs both forward and backwards commands.
        :return: N/A
        """
        '''
        Send to stage:
        <87 5>/r
        Receive from stage:

        '''
        self.send_command('87', [ 5])
        time.sleep(0.2)
        self.send_command('87', [ 4])
        time.sleep(0.2)


    def startup(self):
        """
        TODO Runs the New Scale recommended startup sequence. This is not yet complete. See New Scale docs, page 7.
        :return: NA
        """
        #forwardStep = ['0x31', '0x20', '0x30', '0x30', '0x30', '0x30', '0x30', '0x30', '0x36', '0x34']  # [1 000000064]
        ##backwardStep =
        #self.send_command('06', ['0x31'] + ['0x20'] + encoder_convert(64))
        self.send_command('06', [48] + [32] + encode_to_command(100))
        self.send_command('06', [49] + [32] + encode_to_command(100))
        # self.calibrate()  # TODO Turn this back on


    def get_closed_loop_speed(self):
        """Get Close Loop Speed information
        return close loop speed
        """
        self.send_command_no_vars('40')
        time.sleep(0.2)
        temp = self.read()
        print('This is speed',temp)


    def go_to_location(self, location):
        """
        Sends the stage to the location specified, in encoder counts
        :param location: a location in encoder counts
        :return: NA
        """

        #print(encode_to_command(location)) ###FOR DEBUGGING PURPOSES######

        self.send_command('08', encode_to_command(location))


    def move_steps(self,steps):

        self.send_command('06',[48] + [32] + encode_to_command(steps))


    def return_home(self):
        """
        Funtion that sends the stage to its home location
        :return: NA
        """
        self.go_to_location(self.home)


    def open_loop(self):  # NOTE Come back to later.
        """Set the stage into open loop mode
        :return NA
        """
        self.send_command('20', [48])


    def view_mode(self):  # NOTE Come back to later.
        """View the current Mode
        return the current mode information
        """
        self.send_command('20', [82])
        time.sleep(0.2)
        temp = self.read()
        print('This is the mode',temp)


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





