from setup import *

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

	return x, y, z

# This also flips the y value when converting from 3d to 2d space.
def flatten(x, y, z):
	y *= -1
	return x/z, y/z

# We should move this function later, **not to setup**.
def pointToPixel(point):

	# Get the size of the window
	# root.update()
	width = canvas.winfo_width()
	height = canvas.winfo_height()

	# Get the coordinates in pixels based on the window width and height
	# This should let the window be stretchable
	x = (width/2)  + (width/2)  * point[0]
	y = (height/2) + (height/2) * point[1]

	return x, y


def polygon(*args, **kwargs):
	for v in args:
		v.x -= camera.x
		v.y -= camera.y
		v.z -= camera.z
	newVerticies = []
	cutoff = 0.25
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
						interpoint = intersection(0, 0, 1, -cutoff, args[i].x, args[i].y, args[i].z, neighbour.x, neighbour.y, neighbour.z)
						newVerticies.append(Vector(interpoint[0], interpoint[1], interpoint[2]))
			else:
				newVerticies.append(args[i])

		if(newVerticies):
			return canvas.create_polygon(
				[pointToPixel(flatten(vertex.x, vertex.y, vertex.z)) for vertex in newVerticies],
				kwargs
			)
	return None