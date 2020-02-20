class World:

	def __init__(self, *polygons):
		self.mesh = polygons

	def draw(self, translation, rotation):
		for polygon in self.mesh:
			polygon.draw(translation, rotation)

class Racetrack(World):

	def __init__(self, level):
		pass