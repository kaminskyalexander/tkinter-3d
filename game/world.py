from game.setup import *
from game.bsp import buildSubtree
from game.geometry import findPolygonNormal, getDotProduct, normalize, vectorSum
from core.util import getNeighbours, sortQuad, angleAverage, find2dLineAngle, rotate2dLine
from game.light import Light

class World:

	def __init__(self, *polygons):
		self.mesh = list(polygons)
		self.tree = buildSubtree(self.mesh)
		self.light = Light(Vector(0, 0, 0))

	def extend(self, world):
		self.mesh.extend(world.mesh)
		self.tree = buildSubtree(self.mesh)

	def draw(self, translation, rotation, tree = None):
		if tree == None: tree = self.tree

		tree.polygon.apply(translation, rotation)
		normal = normalize(findPolygonNormal(tree.polygon))

		center = vectorSum(tree.polygon.frame) / len(tree.polygon.frame)
		direction = getDotProduct(normal, Vector(0, 0, 0) - tree.polygon.frame[0])

		lightDirection = normalize(self.light.position - center)

		intensity = getDotProduct(normal, lightDirection)
		intensity = max(0, intensity) if direction > 0 else max(0, -intensity)

		tree.polygon.properties["fill"] = "#{0:02X}{0:02X}{0:02X}".format(int(intensity*128 + 64))

		if direction > 0:
			if tree.back: self.draw(translation, rotation, tree.back)
			tree.polygon.draw()
			if tree.front: self.draw(translation, rotation, tree.front)
		else:
			if tree.front: self.draw(translation, rotation, tree.front)
			tree.polygon.draw()
			if tree.back: self.draw(translation, rotation, tree.back)

# https://www.scratchapixel.com/lessons/3d-basic-rendering/introduction-to-shading/diffuse-lambertian-shading
# https://www.davrous.com/2013/07/03/tutorial-part-5-learning-how-to-write-a-3d-software-engine-in-c-ts-or-js-flat-gouraud-shading/