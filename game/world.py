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