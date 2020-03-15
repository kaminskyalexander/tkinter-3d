from game.setup import *
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
		DEBUG_TRANSFORM_ROTATE_TIME = time()
		for polygon in self.mesh:
			polygon.apply(translation, rotation)
		debugger.record("Transformation/Rotation", time() - DEBUG_TRANSFORM_ROTATE_TIME)

		DEBUG_BSP_SORT_TIME = time()
		tree = traverse(buildSubtree(self.mesh))
		debugger.record("BSP Sort", time() - DEBUG_BSP_SORT_TIME)

		import game.polygon
		
		for polygon in tree:
			polygon.draw()
		debugger.record("Polygon Culling", game.polygon.DEBUG_POLY_CULL_TIME)
		debugger.record("Polygon Drawing", game.polygon.DEBUG_POLY_DRAW_TIME)
		game.polygon.DEBUG_POLY_CULL_TIME = 0
		game.polygon.DEBUG_POLY_DRAW_TIME = 0