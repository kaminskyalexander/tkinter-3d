from game.editor.setup import *
from core.inputs import InputListener
from core.util import getNeighbours
from math import *

inputs = InputListener(root)
debug = True

vertices = []
ROAD_WIDTH = 50

def update():
	global rotation
	start = int(time() * 1000)

	inputs.refresh()
	canvas.delete("frame")

	if inputs.key(82, "press"): vertices.clear() # R to reset

	if inputs.button(1, "release"):
		vertices.append(inputs.motion)

	edges = []

	for i, vertex in enumerate(vertices):
		canvas.create_oval(
			vertex[0] - 5, vertex[1] - 5,
			vertex[0] + 5, vertex[1] + 5,
			fill = "green" if i == 0 else "red",
			tag = ("frame", "vertex")
		)
		
		prevPoint = vertices[i-1] if i != 0 else vertices[-1]
		canvas.create_line(
			vertex[0], vertex[1],
			prevPoint[0], prevPoint[1],
			fill = "white",
			tag = ("frame", "line")
		)
		rotate90 = True
		if len(vertices) > 1:
			previous, after = getNeighbours(i, vertices)

			xdiff1 = previous[0] - vertex[0]
			ydiff1 = previous[1] - vertex[1]
			xdiff2 = vertex[0]   - after[0]
			ydiff2 = vertex[1]   - after[1]
			
			if(xdiff1 == 0 or xdiff2 == 0):
				rotate90 = False
				angle = 0
			else:
				# If slope of one line is positive and the other lines slope is negative
				if(ydiff1/xdiff1 > 0 and ydiff2/xdiff2 < 0) or (ydiff2/xdiff2 > 0 and ydiff1/xdiff1 < 0):
					# If theres one above and one below
					if(previous[1] < vertex[1] < after[1] or after[1] < vertex[1] < previous[1]):
						rotate90 = False
				angle1 = atan(ydiff1 / xdiff1)
				angle2 = atan(ydiff2 / xdiff2)
				angle = (angle1 + angle2) / 2
		else:
			angle = pi/2

		x1 = cos(angle + pi*0.5 if rotate90 else angle) * ROAD_WIDTH + vertex[0]
		y1 = sin(angle + pi*0.5 if rotate90 else angle) * ROAD_WIDTH + vertex[1]
		x2 = cos(angle + pi*1.5 if rotate90 else angle + pi) * ROAD_WIDTH + vertex[0]
		y2 = sin(angle + pi*1.5 if rotate90 else angle + pi) * ROAD_WIDTH + vertex[1]

		edges.append(((x1, y1), (x2, y2)))

	for i, edge in enumerate(edges):
		if i != 0:
			canvas.create_polygon(
				edges[i][0][0],   edges[i][0][1],
				edges[i][1][0],   edges[i][1][1],
				edges[i-1][1][0], edges[i-1][1][1],
				edges[i-1][0][0], edges[i-1][0][1],
				fill = "gray",
				outline = "red",
				width = 2,
				tag = "frame"
			)
		else:
			canvas.create_polygon(
				edges[i][0][0],   edges[i][0][1],
				edges[i][1][0],   edges[i][1][1],
				edges[-1][0][0], edges[-1][0][1],
				edges[-1][1][0], edges[-1][1][1],
				fill = "gray",
				outline = "red",
				width = 2,
				tag = "frame"
			)


	canvas.tag_raise("vertex")
	canvas.tag_raise("debug")

	wait = int(time() * 1000) - start
	rate = 1000 // framerate
	delay = rate - wait if rate - wait < rate else rate
	if(delay < 1): delay = 1

	if(debug):
		canvas.create_text(
			10, 10,
			text = """\
Racetrack Editor / Test
Inputs: {}
Limit: {}
Wait: {}
Rate: {}
Delay: {}
""".format(
				inputs.inputs,
				framerate,
				wait,
				rate,
				delay
			),
			font = ("Consolas", 11, ""),
			fill = "white",
			anchor = "nw",
			tag = ("frame", "debug")
		)

	canvas.after(delay,	update)

update()
tk.mainloop()
