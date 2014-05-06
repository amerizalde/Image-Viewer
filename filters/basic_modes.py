
### MODIFY PER CHANNEL ###
# A is the active layer,
# B is a composite of the layers underneath A.
#
# The input should be the pixel luminance normalized to (0.0 .. 1.0)

def multiply(a, b):
	return (a * b)

def color_burn(a, b):
	return (1 - (1 - b) / a)

def linear_burn(a, b):
	return (a + b - 1)

def screen(a, b):
	return (1 - (1 - a) * (1 - b))

def color_dodge(a, b):
	return (b / (1 - a))

def linear_dodge(a, b):
	return (a + b)

def subtract(a, b):
	return (b - a)

def divide(a, b):
	return (b / a)

def darken(a, b):
	return min(a, b)

def lighten(a, b):
	return max(a, b)