from game.setup import *
from game.geometry import rotate

class Light:

	def __init__(self, position, intensity = None):
		self.position = position
		self.frame = self.position
		self.intensity = intensity

	def apply(self, translation, rotation):
		self.frame = rotate(self.position - translation, rotation)
