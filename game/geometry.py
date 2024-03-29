from game.setup import *
from core.util import getNeighbours

def flip(vector):
	x, y, z = vector.x*-1, vector.y*-1, vector.z*-1
	return Vector(x, y, z)

# Find the normal of three points
def findNormal(vector1, vector2, vector3):

	# Find cross product of two sides
	v = vector2 - vector1
	w = vector3 - vector1
	x = (v.y * w.z) - (v.z * w.y)
	y = (v.z * w.x) - (v.x * w.z)
	z = (v.x * w.y) - (v.y * w.x)

	return Vector(x, y, z)

def findPolygonNormal(polygon):
	if len(polygon.frame) > 2:
		return findNormal(
			polygon.frame[0],
			polygon.frame[1],
			polygon.frame[2]
		)

# Returns on a scale from -1 to 1
def getDotProduct(vector1, vector2):
	return round(sum(vector1 * vector2), 5)

def normalize(vector):
	length = sqrt(vector.x**2 + vector.y**2 + vector.z**2)
	if length == 0: return vector
	else: return vector / length

def vectorSum(vectors):
	result = Vector(0, 0, 0)
	for vector in vectors:
		result += vector
	return result

def intersection(a, b, c, d, x1, y1, z1, x2, y2, z2):

	# Solve for T by using "Ax + By + Cz + D = 0" and subbing in the 
	# parametric linear equation given by the x y and z parameters.
	t = (
		(a*x1 + b*y1 + c*z1 + d) /
		(a*x2 - a*x1 + b*y2 - b*y1 + c*z2 - c*z1)
	)

	# Now that we know t, we can find the point of intersection.
	x = x1 - (x2 - x1) * t
	y = y1 - (y2 - y1) * t
	z = z1 - (z2 - z1) * t

	return Vector(x, y, z)

# This also flips the y value when converting from 3d to 2d space.
def flatten(vector):
	x, y, z = vector.x, vector.y * -1, vector.z
	return x/z, y/z

def pointToPixel(point):

	# Get the size of the window
	width = canvas.winfo_width()
	height = canvas.winfo_height()

	# Get the coordinates in pixels based on the window width and height
	# This should let the window be stretchable
	x = (width/2  + offset.x) + (height/2) * point[0]
	y = (height/2 + offset.y) + (height/2) * point[1]

	return x, y

# Reference: https://math.stackexchange.com/a/1741317
def rotationMatrix(vector):
	x = (vector.x/360) * (pi * 2)
	y = (vector.y/360) * (pi * 2)
	z = (vector.z/360) * (pi * 2)
	matrix = [
		[
			cos(y)*cos(z),
			cos(x)*sin(z) + sin(x)*sin(y)*sin(z),
			sin(x)*sin(z) - cos(x)*sin(y)*cos(z)
		],
		[
			-cos(y)*sin(z),
			cos(x)*cos(z) - sin(x)*sin(y)*sin(z),
			sin(x)*cos(z) + cos(x)*sin(y)*sin(z)
		],
		[
			sin(y),
			-sin(x)*cos(y),
			cos(x)*cos(y)
		]
	]
	return matrix

# Takes in a point vector and a rotation vector
# Calculation is relative to the origin
def rotate(vector, matrix):
	A = matrix
	new = Vector(
		A[0][0]*vector.x + A[0][1]*vector.y + A[0][2]*vector.z,
		A[1][0]*vector.x + A[1][1]*vector.y + A[1][2]*vector.z,
		A[2][0]*vector.x + A[2][1]*vector.y + A[2][2]*vector.z
	)
	return new

def cull(*args):
	vertices = args[:]
	# How close to the screen should objects be culled
	cutoff = 0.25
	# How far away from the screen objects should be culled
	renderDistance = 20

	# Plane equations
	# (a, b, c, d values for "Ax + By + Cz + D = 0")
	widthRatio = 1/(canvas.winfo_width()/canvas.winfo_height())
	planes = {
		"behind": (0, 0, 1, -cutoff),
		"ahead":  (0, 0, 1, -renderDistance),
		"top":    (0, 1, -1, 0),
		"bottom": (0, 1, 1, 0),
		"left":   (widthRatio, 0, 1, 0),
		"right":  (widthRatio, 0, -1, 0)
	}

	for direction in planes:
		new = []
		for i, vertex in enumerate(vertices):
			neighbours = getNeighbours(i, vertices)

			# Detect if the vertex is outside the frustum (viewable area)
			if(
				(direction == "behind" and vertices[i].z <  cutoff) or
				(direction == "ahead"  and vertices[i].z >  renderDistance) or
				(direction == "top"    and vertices[i].y >  vertices[i].z) or
				(direction == "bottom" and vertices[i].y < -vertices[i].z) or
				(direction == "left"   and vertices[i].x*widthRatio < -vertices[i].z) or
				(direction == "right"  and vertices[i].x*widthRatio >  vertices[i].z)
			):
				for neighbour in neighbours:
					# Detect if the vertex has a neighbouring point inside the frustum
					if(
						(direction == "behind" and not neighbour.z <  cutoff) or
						(direction == "ahead"  and not neighbour.z >  renderDistance) or
						(direction == "top"    and not neighbour.y >  neighbour.z) or
						(direction == "bottom" and not neighbour.y < -neighbour.z) or
						(direction == "left"   and not neighbour.x*widthRatio < -neighbour.z) or
						(direction == "right"  and not neighbour.x*widthRatio >  neighbour.z)
					):
						# If the point has a neighbour, find where the edge connecting the
						# two points intersects the plane to "slice" the shape along the
						# edge of the frustum
						new.append(
							intersection(
								*planes[direction], 
								*vertices[i],
								*neighbour
							)
						)
			else: new.append(vertices[i])
		# Reset the state for the next direction
		vertices = new[:]

	return new

# **** DEPRECATED AND LESS EFFICIENT *****
# Draws a polygon in 3D space
# Takes in vectors as arguments and effects to apply
# to the shape as keyword arguments in the same format
# as Tkinter's canvas.create_polygon()
def polygon(camera, rotation, *args, debug = False, **kwargs):
	args = list(args)
	
	# Find the rotation matrix and apply it onto all points
	matrix = rotationMatrix(rotation)
	for i, vertex in enumerate(args):
		# Apply camera position and rotation
		args[i] = rotate(vertex - camera, matrix)

	vertices = cull(*args)
	if(vertices):

		# Debug text
		if(debug):
			DEBUG_TEXT = ""
			for vertex in vertices:
				DEBUG_TEXT += (
					str(vertex.x) + "\n" + 
					str(vertex.y) + "\n" +
					str(vertex.z) + "\n\n"
				)
			canvas.create_text(
				pointToPixel(flatten(vertices[0])),
				text = DEBUG_TEXT,
				font = ("System", 11, ""),
				tag = ("frame", "debug")
			)
		
		# Draw the shape
		return canvas.create_polygon(
			[pointToPixel(flatten(vertex)) for vertex in vertices],
			kwargs,
			tag = "frame"
		)