from game.setup import *
from game.geometry import getDotProduct, findNormal, intersection
from game.polygon import Polygon

class Node:
	def __init__(self, polygon):
		self.polygon = polygon
		self.front = None
		self.back = None

def buildSubtree(polygons):
	polygons = polygons[:]
	if polygons:
		rootPoly = polygons[0]
		polygons.remove(rootPoly)
		rootNode = Node(rootPoly)

		# Find normal vector of root polygon
		normal = findNormal(*rootPoly.vertices[:3])
		# Values for plane equation of root polygon
		a, b, c = normal
		d = -(rootPoly.vertices[0].x * a + rootPoly.vertices[0].y * b + rootPoly.vertices[0].z * c)

		frontList = []
		backList = []
		for p in polygons:
			# Determines if each vertex is in front of or behind the root polygon
			sides = []
			for vertex in p.vertices:
				dp = Vector.dot(normal, (vertex - rootPoly.vertices[0]))
				if dp > 0:
					sides.append(1)
				elif dp < 0:
					sides.append(0)
				else:
					sides.append(None)

			# In front
			if 1 in sides and not 0 in sides:
				frontList.append(p)

			# Behind
			elif 0 in sides and not 1 in sides:
				backList.append(p)

			# Intersecting
			else:
				toggle = 0
				splitPolygon = [[],[]]

				for i, vertex in enumerate(p.vertices):
					before = p.vertices[i - 1]
					# If the edge is not intersecting the plane
					if sides[i] == sides[i - 1]:
						splitPolygon[toggle].append(before)
					else:
						poi = intersection(a, b, c, d, *before, *vertex)
						splitPolygon[toggle].append(before)
						splitPolygon[toggle].append(poi)
						toggle = 1 if not toggle else 0
						splitPolygon[toggle].append(poi)
				# Check which direction the part of split polygon is on (determine the order)
				if Vector.dot(normal, (splitPolygon[0][0] - rootPoly.vertices[0])) > 0:
					if splitPolygon[0]: frontList.append(Polygon(p.canvas, *splitPolygon[0], debug = p.debug, **p.properties))
					if splitPolygon[1]: backList.append(Polygon(p.canvas, *splitPolygon[1], debug = p.debug, **p.properties))
				else:
					if splitPolygon[0]: backList.append(Polygon(p.canvas, *splitPolygon[0], debug = p.debug, **p.properties))
					if splitPolygon[1]: frontList.append(Polygon(p.canvas, *splitPolygon[1], debug = p.debug, **p.properties))
		if frontList: rootNode.front = buildSubtree(frontList)
		if backList: rootNode.back = buildSubtree(backList)
		return rootNode