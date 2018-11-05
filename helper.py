'''
This file contains helper functions that are used by Stage, StageSPI, as well as the main function
Last Modified: R. Nance 5/15/2018
#####################DO NOT EDIT BELOW INFORMATION##################################
Originating Branch: Master
Originally Created: R. Nance 03/2018
'''

import pygame
from main import x_axis, y_axis, z_axis




def encode_to_command(value):
    """
    Builds the guts of a command to send the stage to a particular encoder count
    Steps to figure out what should be converted in order to for command to word
    1. Come up with command according to newscale documentation and write out the command as a series of individual
    chars

    2. convert each character into its hex representation

    3. The command can either be sent as the string of these values, or as the individual decimal values for each
    :param: value: integer between 0 and 12000, representing the encoder count of the location to travel to.
    :return: the 8 bit output that represents
    """
    encode_output = []  # create a blank list to hold the output
    hex_value = hex(int(value)).upper()  # convert the decimal to hex
    value_convert = hex_value[2:]  # remove the 0x from the hex value
    
    # for each character in the input, convert it to its base 10 representation of the ascii character
    for i in value_convert:
        encode_output += [ord(str(i))]
    # ensure that the output is 8 bytes
    for i in range(8 - int(len(encode_output))):  # pads with zeros for len(encode_output) < 8
        encode_output.insert(0, 0x30)
    return encode_output


def encode_to_command4digit(value):
    """
    Builds the guts of a command to send the stage to a particular encoder count
    Steps to figure out what should be converted in order to for command to word
    1. Come up with command according to newscale documentation and write out the command as a series of individual
    chars

    2. convert each character into its hex representation

    3. The command can either be sent as the string of these values, or as the individual decimal values for each
    :param value: integer between 0 and 12000, representing the encoder count of the location to travel to.
    :return: the 8 bit output that represents
    """
    encode_output = []  # create a blank list to hold the output
    hex_value = hex(int(value)).upper()  # convert the decimal to hex
    value_convert = hex_value[2:]  # remove the 0x from the hex value
    
    # for each character in the input, convert it to its base 10 representation of the ascii character
    for i in value_convert:
        encode_output += [ord(str(i))]
    # ensure that the output is 8 bytes
    for i in range(4 - int(len(encode_output))):
        encode_output.insert(0, 0x30)
    return encode_output


def encoder_convert(value):
    '''
    THIS FUNCTION IS NOW DEPRECATED BUT HAS NOT YET BEEN REMOVED FROM CIRCULATION. PLEASE DO NOT USE
    Function that takes in a value in decimal and outputs the hex ascii version of it, by taking each number of the hex
    value and sending that digit as a hex number
    '''
    
    hex_value = hex(int(value)).upper() #convert the decimal to hex
    value_convert = hex_value[2:]#remove the 0x from the hex value
    encode_output = []
    for i in str(value_convert):
        encode_output += [hex(ord(i))]
    
    # ensure that the output is 8 bytes
    for i in range(8 - int(len(encode_output))):
        encode_output.insert(0, '0x30')
    
    print('Encoded output is ')
    print('EncoderCount Output', encode_output)
    print(encode_output[1] + encode_output[2])
    
    return encode_output
## deprecated function

def hex_to_command(command):
    """From heximal number to 6 digit command
    """
    encode_output = []
    for i in command:
        encode_output += [ord(str(i))]
    
    # ensure that the output is 8 bytes
    for i in range(6 - int(len(encode_output))):
        encode_output.insert(0, 0x30)  # after each zero, insert a space
    return encode_output


def hex_to_command4(command):
    """From heximal number to 4 digit command
        """
    encode_output = []
    for i in command:
        encode_output += [ord(str(i))]
    # ensure that the output is 8 bytes
    for i in range(4 - int(len(encode_output))):
        encode_output.insert(0, 0x30)
    return encode_output


def hex_to_command2(command):
    """From hexadecimal number to 2 digit command
        """
    encode_output = []
    for i in command:
        encode_output += [ord(str(i))]
    # ensure that the output is 8 bytes
    for i in range(2 - int(len(encode_output))):
        encode_output.insert(0, 0x30)
    return encode_output


def command_to_string(command):
    """
    Function that prints user readable information to the console. THis is not necessary for operation, however it is
    helpful for readability and debugging purposes
    :param command: a command in the form of a list of hex values that correspond to the ascii characters for the
    command
    :return: String that represents the command sent
    """
    #print(command) ###FOR DEBUGGING PURPOSES ONLY###
    string_out = ''.join(map(chr, command))
    return string_out


def map_val(x, in_min, in_max, out_min, out_max):  # TODO I still have no idea how/why this works. --Jacquelyn
    """
    Maps a value in one range to a value in another range. This code is used in the joystick package
    :param x: value to be mapped
    :param in_min: minimum of the input scale
    :param in_max: maximum of the input scale
    :param out_min: minimum of the output scale
    :param out_max: maximum of the output scale
    :return: mapped value, rounded to the nearest integer value
    """
    return int(round((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min, 0))  # The '0' specifies int output


##########################################OLD CODE THAT IS NOW DEPRICATED#####################



###########################

#
# def encoderCountConvert(value):
#     '''
#     Builds the guts of a command to send the stage to a particular encoder count
#     Steps to figure out what should be converted in order to for command to word
#     1. Come up with command according to newscale documentation and write out the command as a series of individual chars
#     2. convert each character into its hes representation
#     3. The command can either be sent as the string of these values, or as the individual decimal values for each
#     :param value: integer between 0 and 12000, representing the encoder count of the location to travel to.
#     :return: the 8 bit output that represents
#     '''
#
#     encode_output = [] # create a blank list to hold the output
#     hex_value = hex(int(value)).upper()  # convert the decimal to hex
#     value_convert = hex_value[2:]  # remove the 0x from the hex value
#     # print(value_convert)
#     # for each character in the input, convert it to its base 10 representation of the ascii character
#     for i in value_convert:
#         encode_output += [ord(str(i))]
#     # ensure that the output is 8 bytes
#     for i in range(8 - int(len(encode_output))):
#         encode_output.insert(0, 30)
#     # print(encode_output)
#
#     #print('EncoderCOunt OUtput', encode_output)
#     #print(encode_output[1] + encode_output[2])
#     return encode_output
#

def centerAllStages(axis1, axis2, axis3):


    """
    Sends all stages to their central location.
    :param axis1: the first stage
    :param axis2: second stage
    :param axis3: third stage
    :return: na
    """
    #map(Stage.go_to_location(), )
    Stage.go_to_location(axis1, 6000)
    Stage.go_to_location(axis2, 6000)
    Stage.go_to_location(axis3, 6000)


def map_val(x, in_min, in_max, out_min, out_max):
    """
    Maps a value in one range to a value in another range. This code is used in the joystick package
    :param x: value to be mapped
    :param in_min: minimum of the input scale
    :param in_max: maximum of the input scale
    :param out_min: minimum of the output scale
    :param out_max: maximum of the output scale
    :return: mapped value, rounded to the nearest integer value
    """
    return int(round((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min, 0))


def AudioNoti(x,y,xMin,xMax,yMin,yMax):
    "Play Audio Notification when hit the boundary"
    if x == xMin or x == xMax or y == yMin or y == yMax:
        print('Hit the boundary')
        pygame.mixer.init()
        pygame.mixer.music.load("37210703.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():  # Queries whether .play() is still running; if not, continues the loop.
            continue


def statusinfo(status):
    """Status information corresponds to that table in Reference Manual <10>"""
    if status[0] == '1':
        print('The position error exceeds the stall detection threshold while motor is running')
    if status[3] == '1':
        print('Maintenance mode enabled')
    if status[4] == '1':
        print('Motor moving towards target position')
    if status[7] == '1':
        print('Encoded Error occur')
    if status[8] == '1':
        print('Background job active')
    if status[13] == '1':
        print('Reverse travel limit reached')
    if status[14] == '1':
        print('Forward travel limit reached')
    if status[20] == '1':
        print('Motor Communication ok')
    if status[20] == '0':
        print('Motor Communication not good')
    if status[21] == '1':
        print('Motor is running')
    if status[21] == '0':
        print('Motor is not running')
    if status[22] == '1':
        print('Motor going forward')
    if status[22] == '0':
        print('Motor going backward')


def sensitivity_read():
    file = open("sensitivity.txt", "r")
    return file.read()


def sensitivity_write(scale_input):
    f = open("sensitivity.txt", "w+")
    f.truncate()
    f.write(str(scale_input))


        #####################TEST CODE ######################################



#print('This is a test')
#start = input('Please indicate an initial position for the stage')
#x_axis = Stage('0x63', start, 1)
#print(x_axis.get_position())



#value = input('Type a value in')
#print(encoder_convert(value))
#testing = encoder_convert(value)
#print(testing[0])
#commandTest = build_command('0x33', '08', encoder_convert(x_axis.get_position()))
#print(commandTest)



#configuration utility that overwrites
#utility to get configuration code

