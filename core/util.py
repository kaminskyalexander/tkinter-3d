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