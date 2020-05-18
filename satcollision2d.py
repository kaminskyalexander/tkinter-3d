# SAT Collision in 2D example

import tkinter as tk
import math
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])

root = tk.Tk()
canvas = tk.Canvas(root, width = 600, height = 600, bg = "white")
canvas.pack()

polygon1 = [
	Point(100, 100),
	Point(100, 200),
	Point(200, 200),
	Point(200, 100)
]
polygon2 = [
	Point(200, 110),
	Point(125, 185),
	Point(200, 260)
]

def normalize2d(vector):
	magnitude = math.sqrt(vector.x**2 + vector.y**2)
	return Point(vector.x / magnitude, vector.y / magnitude)

def dotProduct2d(vector1, vector2):
	return vector1.x * vector2.x + vector1.y * vector2.y
	
def getUniqueNormals(polygon):
	axes = []
	for i in range(len(polygon)):
		# Get the current vertex
		p1 = polygon[i]
		# Get the next vertex
		p2 = polygon[i+1 if i+1 != len(polygon) else 0]
		# Subtract the two to get the edge vector
		edge = Point(p1.x - p2.x, p1.y - p2.y)
		# Get either perpendicular vector
		# (x, y) => (-y, x) or (y, -x)
		normal = Point(-edge.y, edge.x)
		# Make sure the normal is unique
		if Point(normal.x, normal.y) not in axes and Point(-normal.x, -normal.y) not in axes:
			axes.append(normalize2d(normal))
	return axes

def projectShapeOntoAxis(polygon, axis):
	minimum = dotProduct2d(axis, polygon[0])
	maximum = minimum
	for vertex in polygon:
		p = dotProduct2d(axis, vertex)
		if p < minimum: minimum = p
		if p > maximum: maximum = p
	return minimum, maximum

def detectOverlap(projection1, projection2):
	min1, max1 = projection1
	min2, max2 = projection2
	return max1 > min2 and min1 < max2

def getOverlap(projection1, projection2):
	min1, max1 = projection1
	min2, max2 = projection2
	if max1 < max2:
		return max1 - min2
	else:
		return max2 - min1

def satCollision(polygon1, polygon2):
	minimumOverlap = math.inf
	smallestAxis = None
	axes1 = getUniqueNormals(polygon1)
	axes2 = getUniqueNormals(polygon2)

	for axis in axes1 + axes2:
		p1 = projectShapeOntoAxis(polygon1, axis)
		p2 = projectShapeOntoAxis(polygon2, axis)
		if not detectOverlap(p1, p2):
			return False
		else:
			overlap = getOverlap(p1, p2)
			if overlap < minimumOverlap:
				minimumOverlap = overlap
				smallestAxis = axis
	
	return smallestAxis, minimumOverlap		

satInfo = satCollision(polygon1, polygon2)
if satInfo != False: axisRounded = round(satInfo[0].x,3), round(satInfo[0].y,3)
else: axisRounded = None

canvas.create_polygon([(p.x, p.y) for p in polygon1], fill = "red")
canvas.create_polygon([(p.x, p.y) for p in polygon2], fill = "blue", stipple = "gray75")
canvas.create_text(300, 50, font = ("Arial", 10, "bold"), text = f"Collision Axis: {axisRounded}\nCollision Minimum Overlap: {satInfo[1] if satInfo != 1 else None}")

moveAmount = Point(satInfo[0].x * satInfo[1], satInfo[0].y * satInfo[1])
polygon3 = [Point(p.x + moveAmount.x, p.y + moveAmount.y) for p in polygon2]

canvas.create_polygon([(p.x, p.y) for p in polygon3], fill = "black", stipple = "gray50")

root.mainloop()
