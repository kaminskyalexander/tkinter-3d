from tkinter import PhotoImage
from image import Colour, PNG
from copy import deepcopy

# BETTERIMAGE: cause its better than PhotoImage :)
# notes:
# ** if for whatever reason there is the desire to
#    use the garbage methods bundeled with tk's
#    photoimage, you can always x.instance.method()
class BetterImage: 

	# Defines/refreshes the Tkinter PhotoImage object
	# I would use @property for this but memory garbage collection stupid
	def generate(self):
		self.instance = PhotoImage(data = self.image.repackage(), format = "png")

	# Load the image using the PNG class, then generate it
	def __init__(self, filepath):
		self.image = PNG(filepath)
		self.source = deepcopy(self.image)
		self.generate()

	# More like invert; just reverses the row order
	def flip(self):
		self.image.pixels = self.image.pixels[::-1] 
		self.generate()

	# Nearest neighbour interpolation?
	# TODO efficiency because im looping like crazy with bigger pixel counts
	def resize(self, width, height):
		cw, ch = self.source.width, self.source.height
		new = []
		for y in range(height):
			new.append([])
			for x in range(width):
				# Get relative pixels
				relx = round((cw-1) * (x / (width-1)))
				rely = round((ch-1) * (y / (height-1)))
				new[y].append(self.source.pixels[rely][relx])
		self.image.pixels = new
		self.generate()