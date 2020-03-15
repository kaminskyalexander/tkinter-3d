from game.setup import *
from game.geometry import rotate, cull, pointToPixel, flatten

DEBUG_POLY_CULL_TIME = 0
DEBUG_POLY_DRAW_TIME = 0

class Polygon:

	def __init__(self, canvas, *args, debug = False, **kwargs):
		self.canvas = canvas
		self.vertices = list(args)
		self.frame = self.vertices
		self.debug = debug
		self.properties = kwargs

	def apply(self, translation, rotation):
		vertices = self.vertices[:]
		for i, vertex in enumerate(vertices):
			vertices[i] = rotate(vertex - translation, rotation)
		self.frame = vertices

	def draw(self):
		global DEBUG_POLY_CULL_TIME, DEBUG_POLY_DRAW_TIME
		DEBUG_CULL_TIME = time()
		vertices = cull(*self.frame)
		DEBUG_POLY_CULL_TIME += time() - DEBUG_CULL_TIME

		DEBUG_DRAW_TIME = time()
		if vertices:
			self.canvas.create_polygon(
				[pointToPixel(flatten(vertex)) for vertex in vertices],
				self.properties,
				tag = "frame"
			)
		DEBUG_POLY_DRAW_TIME += time() - DEBUG_DRAW_TIME
				