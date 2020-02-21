from game.geometry import rotate, cull, pointToPixel, flatten

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

	# For Painter's Algorithm
	@property
	def distance(self):
		distances = [vertex.z for vertex in self.frame]
		return sum(distances) / len(distances)

	def draw(self):
		vertices = cull(*self.frame)
		if vertices:
			self.canvas.create_polygon(
				[pointToPixel(flatten(vertex)) for vertex in vertices],
				self.properties,
				tag = "frame"
			)
				