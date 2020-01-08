class Vector:

	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

	def add(self, vector):
		self.x += vector.x
		self.y += vector.y
		self.z += vector.z

	def subtract(self, vector):
		self.x -= vector.x
		self.y -= vector.y
		self.z -= vector.z

	def multiply(self, vector):
		self.x *= vector.x
		self.y *= vector.y
		self.z *= vector.z
	
	def divide(self, vector):
		self.x /= vector.x
		self.y /= vector.y
		self.z /= vector.z

	def assign(self, vector):
		self.x = vector.x
		self.y = vector.y
		self.z = vector.z