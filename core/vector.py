class Vector:

	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

	def __add__(self, other):
		return Vector(
			self.x + other.x,
			self.y + other.y,
			self.z + other.z
		)

	def __sub__(self, other):
		return Vector(
			self.x - other.x,
			self.y - other.y,
			self.z - other.z
		)

	def __mul__(self, other):
		return Vector(
			self.x * other.x,
			self.y * other.y,
			self.z * other.z
		)

	def __truediv__(self, other):
		return Vector(
			self.x / other.x,
			self.y / other.y,
			self.z / other.z
		)

	def __str__(self):
		return "({}, {}, {})".format(self.x, self.y, self.z)

	def get(self): 
		return self.x, self.y, self.z

	def __iter__(self):
		return iter((self.x, self.y, self.z))