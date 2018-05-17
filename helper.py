'''
This file contains helper functions that are used by Stage, StageSPI, as well as the main function
Last Modified: R. Nance 5/15/2018
#####################DO NOT EDIT BELOW INFORMATION##################################
Originating Branch: Master
Originally Created: R. Nance 03/2018
'''



def encodeToCommand(value):
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
    encodeOutput = []  # create a blank list to hold the output
    hexValue = hex(int(value)).upper()  # convert the decimal to hex
    valueConvert = hexValue[2:]  # remove the 0x from the hex value
    # for each character in the input, convert it to its base 10 representation of the ascii character
    for i in valueConvert:
        encodeOutput += [ord(str(i))]
    # ensure that the output is 8 bytes
    for i in range(8 - int(len(encodeOutput))):
        encodeOutput.insert(0, 0x30)
    return encodeOutput


def encoderConvert(value):
    ''''
    THIS FUNCTION IS NOW DEPRECATED BUT HAS NOT YET BEEN REMOVED FROM CIRCULATION. PLEASE DO NOT USE
    Function that takes in a value in decimal and outputs the hex ascii version of it, by taking each number of the hex
    value and sending that digit as a hex number
    '''
    hexValue = hex(int(value)).upper() #convert the decimal to hex
    valueConvert = hexValue[2:]#remove the 0x from the hex value
    encodeOutput = []
    for i in str(valueConvert):
        encodeOutput += [hex(ord(i))]
    # ensure that the output is 8 bytes
    for i in range(8 - int(len(encodeOutput))):
        encodeOutput.insert(0, '0x30')
    print('Encoded output is ')
    print('EncoderCOunt OUtput', encodeOutput)
    print(encodeOutput[1] + encodeOutput[2])
    return encodeOutput




def commandToString(command):
    """
    Function that prints user readable information to the console. THis is not necessary for operation, however it is
    helpful for readability and debugging purposes
    :param command: a commmand in the form of a list of hex values that correspond to the ascii characters for the
    commmand
    :return: String that represents the command sent
    """
    #print(command) ###FOR DEBUGGING PURPOSES ONLY###
    stringOut = ''.join(map(chr, command))
    return stringOut


# def mapval(x, inMin, inMax, outMin, outMax):
#     """
#     Maps a value in one range to a value in another range
#     :param x: value to be mapped
#     :param inMin: minimum of the input scale
#     :param inMax: maximum of the input scale
#     :param outMin: minimum of the output scale
#     :param outMax: maximum of the output scale
#     :return: mapped value, rounded to the nearest integer value
#     """
#     return round((x - inMin) * (outMax - outMin) / (inMax - inMin) + outMin)

def mapval(x, inMin, inMax, outMin, outMax):
    """
    Maps a value in one range to a value in another range. This code is used in the joystick package
    :param x: value to be mapped
    :param inMin: minimum of the input scale
    :param inMax: maximum of the input scale
    :param outMin: minimum of the output scale
    :param outMax: maximum of the output scale
    :return: mapped value, rounded to the nearest integer value
    """
    return int(round((x - inMin) * (outMax - outMin) / (inMax - inMin) + outMin, 0))

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
#     encodeOutput = [] # create a blank list to hold the output
#     hexValue = hex(int(value)).upper()  # convert the decimal to hex
#     valueConvert = hexValue[2:]  # remove the 0x from the hex value
#     # print(valueConvert)
#     # for each character in the input, convert it to its base 10 representation of the ascii character
#     for i in valueConvert:
#         encodeOutput += [ord(str(i))]
#     # ensure that the output is 8 bytes
#     for i in range(8 - int(len(encodeOutput))):
#         encodeOutput.insert(0, 30)
#     # print(encodeOutput)
#
#     #print('EncoderCOunt OUtput', encodeOutput)
#     #print(encodeOutput[1] + encodeOutput[2])
#     return encodeOutput
#

def centerAllStages(axis1, axis2, axis3):


    """
    Sends all stages to their central location.
    :param axis1: the first stage
    :param axis2: second stage
    :param axis3: third stage
    :return: na
    """
    #map(Stage.goToLocation(), )
    Stage.goToLocation(axis1, 6000)
    Stage.goToLocation(axis2, 6000)
    Stage.goToLocation(axis3, 6000)


def mapval(x, inMin, inMax, outMin, outMax):
    """
    Maps a value in one range to a value in another range. This code is used in the joystick package
    :param x: value to be mapped
    :param inMin: minimum of the input scale
    :param inMax: maximum of the input scale
    :param outMin: minimum of the output scale
    :param outMax: maximum of the output scale
    :return: mapped value, rounded to the nearest integer value
    """
    return int(round((x - inMin) * (outMax - outMin) / (inMax - inMin) + outMin, 0))




# def centerAllStages(axis1, axis2, axis3):
#     """
#     Sends all stages to their central location.
#     :param axis1: the first stage
#     :param axis2: second stage
#     :param axis3: third stage
#     :return: na
#     """
#     #map(Stage.goToLocation(), )
#     Stage.goToLocation(axis1, 6000)
#     Stage.goToLocation(axis2, 6000)
#     Stage.goToLocation(axis3, 6000)


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
#     encodeOutput = [] # create a blank list to hold the output
#     hexValue = hex(int(value)).upper()  # convert the decimal to hex
#     valueConvert = hexValue[2:]  # remove the 0x from the hex value
#     # print(valueConvert)
#     # for each character in the input, convert it to its base 10 representation of the ascii character
#     for i in valueConvert:
#         encodeOutput += [ord(str(i))]
#     # ensure that the output is 8 bytes
#     for i in range(8 - int(len(encodeOutput))):
#         encodeOutput.insert(0, 30)
#     # print(encodeOutput)
#
#     #print('EncoderCOunt OUtput', encodeOutput)
#     #print(encodeOutput[1] + encodeOutput[2])
#     return encodeOutput
#

# def mapval(x, inMin, inMax, outMin, outMax):
#     """
#     Maps a value in one range to a value in another range
#     :param x: value to be mapped
#     :param inMin: minimum of the input scale
#     :param inMax: maximum of the input scale
#     :param outMin: minimum of the output scale
#     :param outMax: maximum of the output scale
#     :return: mapped value, rounded to the nearest integer value
#     """
#     return round((x - inMin) * (outMax - outMin) / (inMax - inMin) + outMin)
#


##################Deprecated Code#################

# def mapval(x, inMin, inMax, outMin, outMax):
#     """
#     Maps a value in one range to a value in another range
#     :param x: value to be mapped
#     :param inMin: minimum of the input scale
#     :param inMax: maximum of the input scale
#     :param outMin: minimum of the output scale
#     :param outMax: maximum of the output scale
#     :return: mapped value, rounded to the nearest integer value
#     """
#     return round((x - inMin) * (outMax - outMin) / (inMax - inMin) + outMin)


        #####################TEST CODE ######################################





#print('This is a test')
#start = input('Please indicate an initial position for the stage')
#xaxis = Stage('0x63', start, 1)
#print(xaxis.getPosition())



#value = input('Type a value in')
#print(encoderConvert(value))
#testing = encoderConvert(value)
#print(testing[0])
#commandTest = buildCommand('0x33', '08', encoderConvert(xaxis.getPosition()))
#print(commandTest)



#configuration utility that overwrites
#utility to get configuration code

