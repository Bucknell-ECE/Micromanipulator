# From beginning of main.py.

controlMode = 'position'  # TODO Create function to change this to 'velocity' mode
safety_margin = 50  # TODO Change to use M3-LS "Soft Limits"

xlinearRangeMin = 0
xlinearRangeMax = 12000
xlinearRange = 12000
ylinearRangeMin = 0
ylinearRangeMax = 12000
ylinearRange = 12000
constrainedLinearRange = 12000
sensitivity = 50
Zsensitivity = 200
getstatus = 0
scaleInput = 0
x_status = ''
y_status = ''
z_status = ''