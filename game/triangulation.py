from game.setup import *
from core.util import getNeighbours
from game.geometry import findNormal

# Determine the winding order of 2D points
def isClockwise(vertices):
	signedArea = 0
	for i, vertex in enumerate(vertices):
		x1, y1 = vertex
		# Get the vertex after
		x2, y2 = getNeighbours(i, vertices)[1]
		signedArea += (x1 * y2 - x2 * y1)
	
	if signedArea > 0:
		return False
	elif signedArea < 0:
		return True
	else:
		raise Exception("Vertices have area of zero.")

# Arguments a, b, c must be in counter-clockwise order
def isConvex(a, b, c):
	# True if the cross product is greater than zero
	return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]) >= 0

# https://www.mathwarehouse.com/geometry/triangles/area/herons-formula-triangle-area.php
def triangleArea(a, b, c):
	ab = sqrt((a[0] - b[0])**2  + (a[1] - b[1])**2)
	ac = sqrt((a[0] - c[0])**2  + (a[1] - c[1])**2)
	bc = sqrt((b[0] - c[0])**2  + (b[1] - c[1])**2)
	s = (a + b + c) / 2
	return sqrt(s * (s - a) * (s - b) * (s - c))

# https://www.geeksforgeeks.org/check-whether-a-given-point-lies-inside-a-triangle-or-not/
def inTriangle(a, b, c, p):
	return triangleArea(a, b, c) == triangleArea(a, b, p) + triangleArea(a, c, p) + triangleArea(b, c, p)

def triangulate(vertices):

	# A triangle/line cannot be triangulated
	if len(vertices) <= 3:
		return vertices

	normal = findNormal(*vertices[:3]).normalized

	# Find the two "basis vectors" of plane
	i = Vector.cross(normal, Vector(0, 1, 0)).normalized
	j = Vector.cross(i, normal).normalized
	
	# Project the vertices into 2D space
	projected = [(Vector.dot(v, i), Vector.dot(v, j)) for v in vertices]
	vertices = list(zip(projected, vertices))

	# Reverse vertices into CCW winding order
	if isClockwise(projected):
		vertices.reverse()

	triangles = []
	while True:
		triangleCreated = False
		for i, vertex in enumerate(vertices):
			previous, after = getNeighbours(i, vertices)
			a, b, c = previous[0], vertex[0], after[0]
			print(a)
			if isConvex(a, b, c):
				for x in vertices:
					# If a vertex lies in the triangle created
					if (x[0] not in (a, b, c)) and inTriangle(a, b, c, x[0]):
						break
				else:
					triangleCreated = True
					triangles.append((previous[1], vertex[1], after[1]))
					del vertices[i]
		if not triangleCreated:
			break

	return triangles

