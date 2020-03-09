from core.vector import Vector
from core.util import getNeighbours
from game.geometry import findNormal, getDotProduct, intersection

# Root:
root = [
	Vector(-1, -1,  0),
	Vector(-1,  1,  0),
	Vector( 1,  1,  0),
	Vector( 1, -1,  0)
]

normal = findNormal(*root[:3])
a, b, c = normal
d = -(root[0].x * a + root[0].y * b + root[0].z * c)

# Polygon:
polygon = [
	Vector(5, -1, 1),
	Vector(5,  1, 1),
	Vector(5,  1, -1),
	Vector(5, -1, -1)
]


sides = []
for vertex in polygon:
	sides.append(1 if getDotProduct(normal, (vertex - root[0])) > 0 else 0)

if(1 in sides and not 0 in sides):
	print("front")
elif(0 in sides and not 1 in sides):
	print("back")
else:
	toggle = 0
	polygons = [[],[]]
	for i, vertex in enumerate(polygon):
		before = polygon[i - 1]	
		if(sides[i] == sides[i - 1]):
			polygons[toggle].append(before)
		else:
			inter = intersection(a, b, c, d, *before, *vertex)
			polygons[toggle].append(before)
			polygons[toggle].append(inter)
			toggle = 1 if not toggle else 0
			polygons[toggle].append(inter)
	[print(*polygon) for polygon in polygons]
	print("intersecting")