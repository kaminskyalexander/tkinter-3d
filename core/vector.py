from math import sqrt

class Vector:

	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

	@property
	def normalized(self):
		length = sqrt(self.x**2 + self.y**2 + self.z**2)
		if length == 0: return self
		else: return self / length

	def normalize(self):
		self.x, self.y, self.z = self.normalized

	@staticmethod
	def dot(vector1, vector2):
		return round(sum(vector1 * vector2), 5)

	@classmethod
	def cross(cls, vector1, vector2):
		x = (vector1.y * vector2.z) - (vector1.z * vector2.y)
		y = (vector1.z * vector2.x) - (vector1.x * vector2.z)
		z = (vector1.x * vector2.y) - (vector1.y * vector2.x)
		return cls(x, y, z)

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

	def __abs__(self):
		return Vector(
			abs(self.x),
			abs(self.y),
			abs(self.z)
		)

	def __str__(self):
		return "({}, {}, {})".format(self.x, self.y, self.z)

	def __iter__(self):
		return iter((self.x, self.y, self.z))