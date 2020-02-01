from tkinter import PhotoImage
from image import PNG

# Test Wrapper (is using this worth it?)
# best name i could think of lol
class BetterImage: 

	def generate(self):
		self.instance = PhotoImage(data = self.image.repackage(), format = "png").zoom(50) # Zoom for debug

	def __init__(self, filepath):
		self.image = PNG(filepath)
		self.generate()

	def flip(self):
		self.image.flip()
		self.generate()