from math import sin, cos, atan, atan2, pi, radians, degrees

def getNeighbours(index, iterable):
	neighbours = []
	if(index > 0):
		neighbours.append(iterable[index - 1])
	else:
		neighbours.append(iterable[len(iterable) - 1])

	if(index < len(iterable) - 1):
		neighbours.append(iterable[index + 1])
	else:
		neighbours.append(iterable[0])
	return neighbours

def sortQuad(p1, p2, p3, p4):
	def takeX(value): return value[0]
	def takeY(value): return value[1]
	points = [p1, p2, p3, p4]

	# Get the top and bottom points of the shape
	points.sort(key = takeY)
	top, bottom = points[:2], points[2:]

	# Sort from left to right
	top.sort(key = takeX)
	bottom.sort(key = takeX)

	# For when drawing a polygon
	bottom.reverse()

	return [*top, *bottom]

def find2dLineAngle(vector1, vector2):
	x1, y1 = vector1.x, vector1.y
	x2, y2 = vector2.x, vector2.y

	dy = y2 - y1
	dx = x2 - x1

	theta = atan2(dy, dx)
	theta *= 180/pi

	return theta

def rotate2dLine(line, degrees, origin = None):
	angle = degrees*pi/180

	x1, y1 = line[0]
	x2, y2 = line[1]

	if origin != None:
		mx, my = origin
	else:
		mx = (x1 + x2) / 2
		my = (y1 + y2) / 2

	# Use a rotation matrix, centering the point to (0, 0)
	rotated = (
		(
			(cos(angle) * (x1-mx) - sin(angle) * (y1-my)) + mx,
			(sin(angle) * (x1-mx) + cos(angle) * (y1-my)) + my
		),
		(
			(cos(angle) * (x2-mx) - sin(angle) * (y2-my)) + mx,
			(sin(angle) * (x2-mx) + cos(angle) * (y2-my)) + my
		)
	)

	return rotated

def snap(x, interval):
    return interval * round(x/interval)

def angleAverage(*angles):
	x = sum([cos(radians(theta)) for theta in angles])
	y = sum([sin(radians(theta)) for theta in angles])
	return round(degrees(atan2(y, x)))
