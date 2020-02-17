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