from game.setup import *
from game.polygon import Polygon
from core.util import getNeighbours, sortQuad

class World:

	def __init__(self, *polygons):
		self.mesh = polygons

	def draw(self, translation, rotation):
		for polygon in self.mesh:
			polygon.draw(translation, rotation)

class Racetrack(World):

	def __init__(self, canvas, level, altitude = -0.25, width = 50):
		
		# Create track mesh:
		points = level["points"]
		edges = []
		polygons = []

		for i, point in enumerate(points):
			rotate = True

			if len(points) > 1:
				previous, after = getNeighbours(i, points)

				xdiff1 = previous[0] - point[0]
				ydiff1 = previous[1] - point[1]
				xdiff2 = point[0]    - after[0]
				ydiff2 = point[1]    - after[1]

				if(xdiff1 == 0 or xdiff2 == 0):
					rotate = False
					angle = 0

				else:
					# If slope of one line is positive and the other lines slope is negative
					if (ydiff1/xdiff1 > 0 and ydiff2/xdiff2 < 0) or (ydiff2/xdiff2 > 0 and ydiff1/xdiff1 < 0):
						# If theres one above and one below
						if (previous[1] < point[1] < after[1]) or (after[1] < point[1] < previous[1]):
							rotate = False
					angle1 = atan(ydiff1 / xdiff1)
					angle2 = atan(ydiff2 / xdiff2)
					angle = (angle1 + angle2) / 2

			else: angle = pi/2

			x1 = cos(angle + pi*0.5 if rotate else angle)      * width + point[0]
			y1 = sin(angle + pi*0.5 if rotate else angle)      * width + point[1]
			x2 = cos(angle + pi*1.5 if rotate else angle + pi) * width + point[0]
			y2 = sin(angle + pi*1.5 if rotate else angle + pi) * width + point[1]

			edges.append(((x1, y1), (x2, y2)))

		for i, edge in enumerate(edges):
			quad = sortQuad(
				(edges[i][0][0],   edges[i][0][1]  ),
				(edges[i][1][0],   edges[i][1][1]  ),
				(edges[i-1][1][0], edges[i-1][1][1]),
				(edges[i-1][0][0], edges[i-1][0][1]),
			)
			vertices = []
			for vertex in quad:
				vertices.append(
					Vector(vertex[0]/100, altitude, vertex[1]/100)
				)
			polygons.append(Polygon(canvas, *vertices, fill = "#666" if i % 2 == 0 else "#555"))

		super().__init__(*polygons)










# # Create the world
# polygons = []
# for i in range(0, 100):
# 	polygons.append(Polygon(
# 		canvas,
# 		Vector(-0.65, -0.5, (i)/2),
# 		Vector(-0.45, -0.5, (i)/2),
# 		Vector(-0.45, -0.5, (i+1)/2),
# 		Vector(-0.65, -0.5, (i+1)/2),
# 		fill = "darkred" if i % 2 == 0 else "#ddd"
# 	))
# 	polygons.append(Polygon(
# 		canvas,
# 		Vector( 0.45, -0.5, (i)/2),
# 		Vector( 0.65, -0.5, (i)/2),
# 		Vector( 0.65, -0.5, (i+1)/2),
# 		Vector( 0.45, -0.5, (i+1)/2),
# 		fill = "darkred" if i % 2 == 0 else "#ddd"
# 	))
# for i in range(0, 50):
# 	polygons.append(Polygon(
# 		canvas,
# 		Vector(-0.5, -0.5, i),
# 		Vector( 0.5, -0.5, i),
# 		Vector( 0.5, -0.5, i + 1),
# 		Vector(-0.5, -0.5, i + 1),
# 		fill = "#666" if i % 2 == 0 else "#555"
# 	))
# 	polygons.append(Polygon(
# 		canvas,
# 		Vector(-0.6, -0.5, i),
# 		Vector( -200, -0.5, i),
# 		Vector( -200, -0.5, i + 1),
# 		Vector(-0.6, -0.5, i + 1),
# 		fill = "green" if i % 2 == 0 else "darkgreen"
# 	))
# 	polygons.append(Polygon(
# 		canvas,
# 		Vector(0.6, -0.5, i),
# 		Vector( 200, -0.5, i),
# 		Vector( 200, -0.5, i + 1),
# 		Vector(0.6, -0.5, i + 1),
# 		fill = "green" if i % 2 == 0 else "darkgreen"
# 	))
# world = World(*polygons)