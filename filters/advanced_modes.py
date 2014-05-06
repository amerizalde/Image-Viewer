import basic_modes as bm

def crunch(a, b, above, below):
	if a >= 0.5:  # equal to or greater than 50% gray
		above(a, b)
	else:
		below(a, b)

def overlay(a, b):
	# this needs to be halved
	crunch(b, a, bm.screen, bm.multiply)

def soft_light(a, b):
	# this needs to be halved
	crunch(a, b, bm.screen, bm.multiply)

def hard_light(a, b):
	# this needs to be halved
	crunch(a, b, bm.linear_dodge, bm.linear_burn)

def vivid_light(a, b):
	# this needs to be halved
	crunch(a, b, bm.color_dodge, bm.color_burn)

def linear_light(a, b):
	crunch(a, b, bm.linear_dodge, bm.linear_burn)

def pin_light(a, b):
	crunch(a, b, bm.lighten, bm.darken)

def hard_mix(a, b):
	pass