#import Stage
from Stage import *
#import smbus

#bus = smbus.SMBus(1)
#def write(self, command):
    #bus.write_i2c_block_data(self.address, 0, command)
def encoderConvert(value):
    ''''
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