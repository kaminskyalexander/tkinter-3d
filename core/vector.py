class Vector:

	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

	def __add__(self, other):
		if isinstance(other, Vector):
			return Vector(
				self.x + other.x,
				self.y + other.y,
				self.z + other.z
			)
		else:
			return Vector(
				self.x + other,
				self.y + other,
				self.z + other
			)

	def __sub__(self, other):
		if isinstance(other, Vector):
			return Vector(
				self.x - other.x,
				self.y - other.y,
				self.z - other.z
			)
		else:
			return Vector(
				self.x - other,
				self.y - other,
				self.z - other
			)

	def __mul__(self, other):
		if isinstance(other, Vector):
			return Vector(
				self.x * other.x,
				self.y * other.y,
				self.z * other.z
			)
		else:
			return Vector(
				self.x * other,
				self.y * other,
				self.z * other
			)

	def __truediv__(self, other):
		if isinstance(other, Vector):
			return Vector(
				self.x / other.x,
				self.y / other.y,
				self.z / other.z
			)
		else:
			return Vector(
				self.x / other,
				self.y / other,
				self.z / other
			)

	def __neg__(self):
		return self * -1

	def __str__(self):
		return "({}, {}, {})".format(self.x, self.y, self.z)

	def __iter__(self):
		return iter((self.x, self.y, self.z))