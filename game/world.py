from game.setup import *
from game.polygon import Polygon
from game.bsp import buildSubtree
from game.geometry import findNormal, getDotProduct
from core.util import getNeighbours, sortQuad, angleAverage, find2dLineAngle, rotate2dLine

def traverse(tree):
	normal = findNormal(*tree.polygon.frame[:3])
	treeList = []
	if getDotProduct(normal, (Vector(0, 0, 0) - tree.polygon.frame[0])) > 0:
		if tree.back:
			treeList.extend(traverse(tree.back))

		treeList.append(tree.polygon)

		if tree.front:
			treeList.extend(traverse(tree.front))
	else:
		if tree.front:
			treeList.extend(traverse(tree.front))

		treeList.append(tree.polygon)

		if tree.back:
			treeList.extend(traverse(tree.back))

	return treeList

class World:

	def __init__(self, *polygons):
		self.mesh = list(polygons)

	def draw(self, translation, rotation):
		for polygon in self.mesh:
			polygon.apply(translation, rotation)

		tree = traverse(buildSubtree(self.mesh))
		for polygon in tree:
			polygon.draw()

class Racetrack(World):

	def __init__(self, canvas, level, altitude = -0.25, roadWidth = 1.25, bumperWidth = 0.1, bumperAngle = 0):

		# Get the path of the road from the level
		path = []
		for point in level["points"]:
			path.append(Vector(point[0]/100, point[1]/100, 0))

		# Get the mesh coordinates for the racetrack
		edges = {"road": [], "bumper-left": [], "bumper-right": []}
		for i, point in enumerate(path):
			# Get list neighbours
			before, after = getNeighbours(i, path)

			# Find the average angle of the two lines
			angle = angleAverage(find2dLineAngle(before, point), find2dLineAngle(point, after))
			# Make the angle perpendicular to the road
			angle += 90

			# Edges used by the road
			edges["road"].append(
				rotate2dLine(
					(
						(point.x - roadWidth/2, point.y),
						(point.x + roadWidth/2, point.y)
					),
					angle,
					origin = (point.x, point.y)
				)
			)
			# Edges used by the bumper
			edges["bumper-left"].append(
				rotate2dLine(
					(
						(point.x - roadWidth/2, point.y),
						(point.x - roadWidth/2 - bumperWidth, point.y)
					),
					angle,
					origin = (point.x, point.y)
				)
			)
			edges["bumper-right"].append(
				rotate2dLine(
					(
						(point.x + roadWidth/2, point.y),
						(point.x + roadWidth/2 + bumperWidth, point.y)
					),
					angle,
					origin = (point.x, point.y)
				)
			)

		# Generate polygons using edges
		polygons = []
		# Road polygons
		for i, edge in enumerate(edges["road"]):
			polygons.append(Polygon(
				canvas,
				Vector(edges["road"][i][0][0],   altitude, edges["road"][i][0][1]),
				Vector(edges["road"][i][1][0],   altitude, edges["road"][i][1][1]),
				Vector(edges["road"][i-1][1][0], altitude, edges["road"][i-1][1][1]),
				Vector(edges["road"][i-1][0][0], altitude, edges["road"][i-1][0][1]),
				fill = "#666" if i % 2 == 0 else "#555"
			))
		for i, edge in enumerate(edges["bumper-left"]):
			polygons.append(Polygon(
				canvas,
				Vector(edges["bumper-left"][i][0][0],   altitude, edges["bumper-left"][i][0][1]),
				Vector(edges["bumper-left"][i][1][0],   altitude, edges["bumper-left"][i][1][1]),
				Vector(edges["bumper-left"][i-1][1][0], altitude, edges["bumper-left"][i-1][1][1]),
				Vector(edges["bumper-left"][i-1][0][0], altitude, edges["bumper-left"][i-1][0][1]),
				fill = "#c00" if i % 2 == 0 else "#ccc"
			))
		for i, edge in enumerate(edges["bumper-right"]):
			polygons.append(Polygon(
				canvas,
				Vector(edges["bumper-right"][i][0][0],   altitude, edges["bumper-right"][i][0][1]),
				Vector(edges["bumper-right"][i][1][0],   altitude, edges["bumper-right"][i][1][1]),
				Vector(edges["bumper-right"][i-1][1][0], altitude, edges["bumper-right"][i-1][1][1]),
				Vector(edges["bumper-right"][i-1][0][0], altitude, edges["bumper-right"][i-1][0][1]),
				fill = "#c00" if i % 2 == 0 else "#ccc"
			))

		super().__init__(*polygons)
