from game.setup import *
from game.bsp import buildSubtree
from game.geometry import findPolygonNormal, getDotProduct
from core.util import getNeighbours, sortQuad, angleAverage, find2dLineAngle, rotate2dLine

class World:

	def __init__(self, *polygons):
		self.mesh = list(polygons)
		self.tree = buildSubtree(self.mesh)

	def extend(self, world):
		self.mesh.extend(world.mesh)
		self.tree = buildSubtree(self.mesh)

	def draw(self, translation, rotation, tree = None):
		if tree == None: tree = self.tree

		tree.polygon.apply(translation, rotation)
		normal = findPolygonNormal(tree.polygon)
		direction = round(getDotProduct(normal, Vector(0, 0, 0) - tree.polygon.frame[0]), 5)

		if direction > 0:
			if tree.back: self.draw(translation, rotation, tree.back)
			tree.polygon.draw()
			if tree.front: self.draw(translation, rotation, tree.front)
		else:
			if tree.front: self.draw(translation, rotation, tree.front)
			tree.polygon.draw()
			if tree.back: self.draw(translation, rotation, tree.back)