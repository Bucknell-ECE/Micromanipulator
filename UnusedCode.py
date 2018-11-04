## From main.py

# x_axis.send_command('40',hex_to_command('001400')+[32]+hex_to_command('000033')+[32]+hex_to_command('0000CD')+[32]+hex_to_command4('0001'))
# y_axis.send_command('40',hex_to_command('001400')+[32]+hex_to_command('000033')+[32]+hex_to_command('0000CD')+[32]+hex_to_command4('0001'))
# x_axis.send_command('20',[48])
# y_axis.send_command('20',[48])
# x_axis.send_command('20',[82])
# time.sleep(0.2)
# temp = x_axis.read()
# print('This is the mode',temp)
# time.sleep(5)
# x_axis.send_command('40',hex_to_command('000400')+[32]+hex_to_command('00000A')+[32]+hex_to_command('000006')+[32]+hex_to_command4('0001'))
# y_axis.send_command('40',hex_to_command('000400')+[32]+hex_to_command('00000A')+[32]+hex_to_command('000006')+[32]+hex_to_command4('0001'))
# x_axis.send_command('09',hex_to_command2('80'))
# x_axis.send_command('09',hex_to_command2('80'))
# x_axis.send_command_no_vars('09')
# time.sleep(0.2)
# temp1 = x_axis.read()
# print('This is the mode',temp1)
# time.sleep(5)
# print('test1',x_axis.send_command('08',encode_to_command(500)))
# time.sleep(5)



## From main.py, potentially for showing joystick feedback in GUI?

# x_axis.go_to_location(map_val(x, 0, 2000, x_linear_range_min, x_linear_range_max))
# print('map_val', map_val(x, 0, 2000, x_linear_range_min, x_linear_range_max))
# x_axis.go_to_location(map_val(y, 0, 2000, y_linear_range_min, y_linear_range_max))
# print('map_val y ', map_val(y, 0, 2000, y_linear_range_min, y_linear_range_max))

# Move Open Loop Steps
# x_axis.send_command('05', [49] + [32] + encode_to_command4digit(100)+[32]+hex_to_command4('186A')+[32]+hex_to_command4('0C35'))
# # x_axis.send_command('05', [49] + [32] + encode_to_command4digit(1000))
# time.sleep(0.2)
# temp2 = x_axis.read()
# print("This is feedback",temp2)

# x_axis.send_command_no_vars('52')
# time.sleep(0.2)
# temp3 = x_axis.read()
# print("This is interval", temp3)

# x_axis.send_command('05', [49] + [32] + encode_to_command4digit(1000)+[32]+hex_to_command4('186A')+[32]+hex_to_command4('0C35'))

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
        set_bounds()

        x_axis.go_to_location(map_val(joy.get_x(), 0, 1023,100, 11900))# x_linear_range_min, x_linear_range_max))
        #x_axis.go_to_location(map_val(joy.get_y(), 0, 255, y_linear_range_min, y_linear_range_max))

        #time.sleep(0.1)
'''
