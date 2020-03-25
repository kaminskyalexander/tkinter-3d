from game.setup import *
from game.bsp import buildSubtree, traverse
from game.geometry import findNormal, getDotProduct
from core.util import getNeighbours, sortQuad, angleAverage, find2dLineAngle, rotate2dLine

class World:

	def __init__(self, *polygons):
		self.mesh = list(polygons)
		self.tree = buildSubtree(self.mesh)

	def extend(self, world):
		self.mesh.extend(world.mesh)
		self.tree = buildSubtree(self.mesh)

	def draw(self, translation, rotation):

		debugger.start("BSP Traversal")
		order = traverse(self.tree)
		debugger.stop("BSP Traversal")
		
		for polygon in order:
			# TODO: Small issue --> BSP traversal is always one frame behind
			# We need to apply transformation and rotation before or during the traversal
			polygon.apply(translation, rotation)
			polygon.draw()

		debugger.stop("Polygon Transformation")
		debugger.stop("Polygon Culling")
		debugger.stop("Polygon Drawing")