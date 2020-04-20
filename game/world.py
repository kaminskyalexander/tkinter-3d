from core.util import *
from game.bsp import buildSubtree
from game.geometry import findPolygonNormal, getDotProduct, normalize, vectorSum
from game.light import Light
from game.setup import *


class World:

	def __init__(self, *polygons):
		self.mesh = list(polygons)
		self.tree = buildSubtree(self.mesh)
		self.light = Light(Vector(-6, 4, -5))
		self.drawingMode = 0

	def extend(self, world):
		self.mesh.extend(world.mesh)
		self.tree = buildSubtree(self.mesh)

	def draw(self, translation, rotation, tree = None):
		if tree == None: tree = self.tree

		# BUG Light is being translated/rotated more than necessary
		self.light.apply(translation, rotation)
		tree.polygon.apply(translation, rotation)
		normal = findPolygonNormal(tree.polygon).normalized

		center = vectorSum(tree.polygon.frame) / len(tree.polygon.frame)
		direction = Vector.dot(normal, Vector(0, 0, 0) - tree.polygon.frame[0])

		lightDirection = self.light.frame - center
		lightDirection.normalize()

		intensity = Vector.dot(normal, lightDirection)
		intensity = max(0, intensity) if direction > 0 else max(0, -intensity)

		tree.polygon.properties["fill"] = brightenHexColor(tree.polygon.color, intensity*100-80)

		if direction > 0:
			if tree.back: self.draw(translation, rotation, tree.back)
			tree.polygon.draw(mode = self.drawingMode)
			if tree.front: self.draw(translation, rotation, tree.front)
		else:
			if tree.front: self.draw(translation, rotation, tree.front)
			tree.polygon.draw(mode = self.drawingMode)
			if tree.back: self.draw(translation, rotation, tree.back)
