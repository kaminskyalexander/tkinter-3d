from game.geometry import rotate, cull, pointToPixel, flatten

class Polygon:

	def __init__(self, canvas, *args, debug = False, **kwargs):
		self.canvas = canvas
		self.vertices = list(args)
		self.debug = debug
		self.properties = kwargs

	def draw(self, translation, rotation):
		vertices = self.vertices[:]
		for i, vertex in enumerate(vertices):
			vertices[i] = rotate(vertex - translation, rotation)

		vertices = cull(*vertices)
		if vertices:
			self.canvas.create_polygon(
				[pointToPixel(flatten(vertex)) for vertex in vertices],
				self.properties,
				tag = "frame"
			)
				