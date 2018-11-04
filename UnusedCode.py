## From main.py

# x_axis.sendCommand('40',hextocommand('001400')+[32]+hextocommand('000033')+[32]+hextocommand('0000CD')+[32]+hextocommand4('0001'))
# y_axis.sendCommand('40',hextocommand('001400')+[32]+hextocommand('000033')+[32]+hextocommand('0000CD')+[32]+hextocommand4('0001'))
# x_axis.sendCommand('20',[48])
# y_axis.sendCommand('20',[48])
# x_axis.sendCommand('20',[82])
# time.sleep(0.2)
# temp = x_axis.read()
# print('This is the mode',temp)
# time.sleep(5)
# x_axis.sendCommand('40',hextocommand('000400')+[32]+hextocommand('00000A')+[32]+hextocommand('000006')+[32]+hextocommand4('0001'))
# y_axis.sendCommand('40',hextocommand('000400')+[32]+hextocommand('00000A')+[32]+hextocommand('000006')+[32]+hextocommand4('0001'))
# x_axis.sendCommand('09',hextocommand2('80'))
# x_axis.sendCommand('09',hextocommand2('80'))
# x_axis.sendCommandNoVars('09')
# time.sleep(0.2)
# temp1 = x_axis.read()
# print('This is the mode',temp1)
# time.sleep(5)
# print('test1',x_axis.sendCommand('08',encodeToCommand(500)))
# time.sleep(5)



## From main.py, potentially for showing joystick feedback in GUI?

# x_axis.goToLocation(mapval(x, 0, 2000, xlinearRangeMin, xlinearRangeMax))
# print('Mapval', mapval(x, 0, 2000, xlinearRangeMin, xlinearRangeMax))
# x_axis.goToLocation(mapval(y, 0, 2000, ylinearRangeMin, ylinearRangeMax))
# print('mapval y ', mapval(y, 0, 2000, ylinearRangeMin, ylinearRangeMax))

# Move Open Loop Steps
# x_axis.sendCommand('05', [49] + [32] + encodeToCommand4digit(100)+[32]+hextocommand4('186A')+[32]+hextocommand4('0C35'))
# # x_axis.sendCommand('05', [49] + [32] + encodeToCommand4digit(1000))
# time.sleep(0.2)
# temp2 = x_axis.read()
# print("This is feedback",temp2)

# x_axis.sendCommandNoVars('52')
# time.sleep(0.2)
# temp3 = x_axis.read()
# print("This is interval", temp3)

# x_axis.sendCommand('05', [49] + [32] + encodeToCommand4digit(1000)+[32]+hextocommand4('186A')+[32]+hextocommand4('0C35'))

# root=Tk()
# positionx = Label(root, text = ('Postion x is ',x))
# positionx.pack()
# root.update_idletasks()

#
## From main.py, changing control mode between 'velocity' and 'position'.
#

'''
REFRESH_RATE = 20000
lastMillis = 0

#currentMillis = datetime.now().microsecond
currentMillis = time.time() * 1000000
if currentMillis - lastMillis < REFRESH_RATE:
    x = 1
    print('l', lastMillis)
    print(currentMillis)
else:
    print('running')
    lastMillis = currentMillis
    #if controlMode == 'velocity':
        #fsdjfl
    if controlMode == 'position':
        setBounds()

        x_axis.goToLocation(mapval(joy.getX(), 0, 1023,100, 11900))# xlinearRangeMin, xlinearRangeMax))
        #x_axis.goToLocation(mapval(joy.gety(), 0, 255, ylinearRangeMin, ylinearRangeMax))

        #time.sleep(0.1)
'''
