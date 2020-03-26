# Takes in a hex color as a string and returns it as an RGB tuple
# For example: "#FFFF00" returns (255, 255, 0)
# Characters can be uppercase or lowercase
def unhexifyColor(color):
	r = int(color[1:3], 16)
	g = int(color[3:5], 16)
	b = int(color[5:7], 16)
	return r, g, b

# Takes in RGB values as a tuple and returns it as a hex color string
# For example: (255, 0, 255) returns "#FF00FF"
# Characters will be returned as uppercase
def hexifyColor(color):
	return "#{:02X}{:02X}{:02X}".format(*color)

def brightenColor(color, percent):
	multiplier = 1 + percent/100
	if multiplier > 1:
		color = tuple(int(min(value * multiplier, 255)) for value in color)
	elif multiplier < 1:
		color = tuple(int(max(value * multiplier, 0)) for value in color)
	return color

def brightenHexColor(color, percent):
	return hexifyColor(brightenColor(unhexifyColor(color), percent))

print( hexifyColor(unhexifyColor("#ff00cc")) )
print( brightenColor((128, 64, 64), 50) )
print( brightenHexColor("#404040", 100) )
