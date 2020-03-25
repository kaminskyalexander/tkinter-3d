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

		DEBUG_BSP_SORT_TIME = time()
		order = traverse(self.tree)
		debugger.record("BSP Sort", time() - DEBUG_BSP_SORT_TIME)

		import game.polygon
		
		for polygon in order:
			# TODO: Small issue --> BSP traversal is always one frame behind
			# We need to apply transformation and rotation before or during the traversal
			polygon.apply(translation, rotation)
			polygon.draw()

		debugger.record("Polygon Culling", game.polygon.DEBUG_POLY_CULL_TIME)
		debugger.record("Polygon Drawing", game.polygon.DEBUG_POLY_DRAW_TIME)
		game.polygon.DEBUG_POLY_CULL_TIME = 0
		game.polygon.DEBUG_POLY_DRAW_TIME = 0