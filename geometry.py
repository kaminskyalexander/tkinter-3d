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

def getNeighbours(index, verticies):
	neighbours = []
	if(index > 0):
		neighbours.append(verticies[index - 1])
	else:
		neighbours.append(verticies[len(verticies) - 1])

	if(index < len(verticies) - 1):
		neighbours.append(verticies[index + 1])
	else:
		neighbours.append(verticies[0])
	return neighbours

def cull(*args):
	verticies = args[:]
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
		for i, vertex in enumerate(verticies):
			neighbours = getNeighbours(i, verticies)

			# Detect if the vertex is outside the frustum (viewable area)
			if(
				(direction == "behind" and verticies[i].z <  cutoff) or
				(direction == "ahead"  and verticies[i].z >  renderDistance) or
				(direction == "top"    and verticies[i].y >  verticies[i].z) or
				(direction == "bottom" and verticies[i].y < -verticies[i].z) or
				(direction == "left"   and verticies[i].x*widthRatio < -verticies[i].z) or
				(direction == "right"  and verticies[i].x*widthRatio >  verticies[i].z)
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
								*verticies[i].get(),
								*neighbour.get()
							)
						)
			else: new.append(verticies[i])
		# Reset the state for the next direction
		verticies = new[:]

	return new

# Draws a polygon in 3D space
# Takes in vectors as arguments and effects to apply
# to the shape as keyword arguments in the same format
# as Tkinter's canvas.create_polygon()
def polygon(*args, debug = False, **kwargs):

	# Find the rotation matrix and apply it onto all points
	matrix = rotationMatrix(rotation)
	for vector in args:
		# Apply the camera position to each point
		vector.subtract(camera)
		# Apply rotation
		vector.assign(rotate(vector, matrix))

	verticies = cull(*args)
	if(verticies):

		# Debug text
		if(debug):
			DEBUG_TEXT = ""
			for vertex in verticies:
				DEBUG_TEXT += (
					str(vertex.x) + "\n" + 
					str(vertex.y) + "\n" +
					str(vertex.z) + "\n\n"
				)
			canvas.create_text(
				pointToPixel(flatten(verticies[0])),
				text = DEBUG_TEXT,
				font = ("System", 11, ""),
				tag = ("frame", "debug")
			)
		
		# Draw the shape
		return canvas.create_polygon(
			[pointToPixel(flatten(vertex)) for vertex in verticies],
			kwargs,
			tag = "frame"
		)