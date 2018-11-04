# From beginning of main.py.

controlMode = 'position'  # TODO Create function to change this to 'velocity' mode
safety_margin = 50  # TODO Change to use M3-LS "Soft Limits"

x_linear_range_min = 0
x_linear_range_max = 12000
xlinearRange = 12000
y_linear_range_min = 0
y_linear_range_max = 12000
ylinearRange = 12000
constrainedLinearRange = 12000
sensitivity = 50
Zsensitivity = 200
get_status = 0
scale_input = 0
x_status = ''
y_status = ''
z_status = ''