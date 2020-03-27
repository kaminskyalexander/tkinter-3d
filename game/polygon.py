from game.setup import *
from game.geometry import rotate, cull, pointToPixel, flatten

class Polygon:

	def __init__(self, canvas, *args, debug = False, **kwargs):
		self.canvas = canvas
		self.vertices = list(args)
		self.frame = self.vertices
		self.debug = debug
		self.color = kwargs["fill"]
		self.properties = kwargs

	def apply(self, translation, rotation):
		debugger.start("Polygon Transformation")
		vertices = self.vertices[:]
		for i, vertex in enumerate(vertices):
			vertices[i] = rotate(vertex - translation, rotation)
		self.frame = vertices
		debugger.pause("Polygon Transformation")

	def draw(self, mode = 0):
		debugger.start("Polygon Culling")
		vertices = cull(*self.frame)
		debugger.pause("Polygon Culling")

		debugger.start("Polygon Drawing")
		if vertices:
			if mode == 0:
				self.canvas.create_polygon(
					[pointToPixel(flatten(vertex)) for vertex in vertices],
					self.properties,
					tag = "frame"
				)
			elif mode == 1:
				for i, vertex in enumerate(vertices):
					previous = vertices[i-1]
					self.canvas.create_line(
						pointToPixel(flatten(previous)),
						pointToPixel(flatten(vertex)),
						fill = "#0f0",
						tag = "frame"
					)
		debugger.pause("Polygon Drawing")
				