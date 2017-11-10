#import Stage
from Stage import *
#import smbus

#bus = smbus.SMBus(1)
#def write(self, command):
    #bus.write_i2c_block_data(self.address, 0, command)
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
    #ensure that the output is 8 bytes
    for i in range(8 - int(len(encodeOutput))):
        encodeOutput.insert(0, '0x30')
    print('EncoderCOunt OUtput', encodeOutput)
    return encodeOutput

def encoderCountConvert(value):
    '''
    Steps to figure out what should be converted in order to for command to word
    1. Come up with command according to newscale documentation and write out the command as a series of individual chars
    2. convert each character into its hes representation
    3. The command can either be sent as the string of these values, or as the individual decimal values for each
    :param value: integer between 0 and 12000, representing the encoder count of the location to travel to.
    :return: the inner base 10 representations of the hex values.
    '''

    encodeOutput = [] # create a blank list to hold the output
    hexValue = hex(int(value)).upper()  # convert the decimal to hex
    valueConvert = hexValue[2:]  # remove the 0x from the hex value
    # print(valueConvert)
    # for each character in the input, convert it to its base 10 representation of the ascii character
    for i in valueConvert:
        encodeOutput += [ord(str(i))]
    # ensure that the output is 8 bytes
    for i in range(8 - int(len(encodeOutput))):
        encodeOutput.insert(0, 30)
    # print(encodeOutput)
    return encodeOutput




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