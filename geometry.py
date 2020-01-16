from setup import *

def flip(vector):
	x, y, z = vector.x*-1, vector.y*-1, vector.z*-1
	return Vector(x, y, z)

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
	vector.y *= -1
	return vector.x/vector.z, vector.y/vector.z

def pointToPixel(point):

	# Get the size of the window
	width = canvas.winfo_width()
	height = canvas.winfo_height()

	# Get the coordinates in pixels based on the window width and height
	# This should let the window be stretchable
	x = (width/2)  + (height/2) * point[0]
	y = (height/2) + (height/2) * point[1]

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

# The messy implementation of drawing a rectangle
# Takes in vectors as arguments and effects to apply
# to the shape as keyword arguments in the same format
# as Tkinter's canvas.create_polygon()
def polygon(*args, **kwargs):
	global rotation
	matrix = rotationMatrix(rotation)
	for vector in args:
		# Apply the camera position to each point
		vector.x -= camera.x
		vector.y -= camera.y
		vector.z -= camera.z
		# Apply rotation
		vector.assign(rotate(vector, matrix))
	newVerticies = []
	# How close to the screen should objects be culled
	cutoff = 0.25
	# How far away from the screen objects should be culled
	renderDistance = 14
	onScreen = False
	for v in args:
		if(v.z < renderDistance):
			onScreen = True
			break
	if(onScreen):
		for i in range(len(args)):
			if(args[i].z < cutoff):
				neighbours = []
				if(i > 0):
					neighbours.append(args[i - 1])
				else:
					neighbours.append(args[len(args) - 1])

				if(i < len(args) - 1):
					neighbours.append(args[i + 1])
				else:
					neighbours.append(args[0])

				for neighbour in neighbours:
					if(neighbour.z > cutoff):
						newVerticies.append(
							intersection(
								0, 0, 1, -cutoff, # Plane: z = 0.25
								args[i].x, args[i].y, args[i].z,
								neighbour.x, neighbour.y, neighbour.z
							)
						)
			else:
				newVerticies.append(args[i])

		if(newVerticies):
			return canvas.create_polygon(
				[pointToPixel(flatten(vertex)) for vertex in newVerticies],
				kwargs,
				tag = "frame"
			)
	return None

# ROTATION DEBUG ......................................
# if __name__ == "__main__":
# 	DEBUG_POINT = Vector(2, 1, 3)
# 	DEBUG_ROTATION = Vector(0, 0, 0)
# 	DEBUG_VALUE = rotate(DEBUG_POINT, DEBUG_ROTATION)
# 	print(DEBUG_VALUE)