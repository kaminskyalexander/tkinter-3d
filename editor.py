from game.editor.setup import *
from core.inputs import InputListener
from core.util import getNeighbours, sortQuad

inputs = InputListener(root)
debug = True

vertices = []
ROAD_WIDTH = 50

camera = Vector(0, 0, 0)

def update():
	global camera
	start = int(time() * 1000)

	inputs.refresh()
	canvas.delete("frame")

	# Left click: Add vertex
	if inputs.button(1, "release"):
		vertices.append(
			(
				inputs.motion[0] + camera.x,
				inputs.motion[1] + camera.y
			)
		)
		
	# R to reset
	if inputs.key(82, "press"):
		vertices.clear()
		camera = Vector(0, 0, 0)

	if inputs.key(87, "press"): camera.y -= 10 # W: Up
	if inputs.key(65, "press"): camera.x -= 10 # A: Left    
	if inputs.key(83, "press"): camera.y += 10 # S: Down
	if inputs.key(68, "press"): camera.x += 10 # D: Right

	edges = []

	for i, vertex in enumerate(vertices):
		canvas.create_oval(
			vertex[0] - 5 - camera.x, vertex[1] - 5 - camera.y,
			vertex[0] + 5 - camera.x, vertex[1] + 5 - camera.y,
			fill = "green" if i == 0 else "red",
			tag = ("frame", "vertex")
		)
		
		prevPoint = vertices[i-1] if i != 0 else vertices[-1]
		canvas.create_line(
			vertex[0] - camera.x, vertex[1] - camera.y,
			prevPoint[0] - camera.x, prevPoint[1] - camera.y,
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
		canvas.create_polygon(
			sortQuad(
				(edges[i][0][0]-camera.x,   edges[i][0][1]-camera.y),
				(edges[i][1][0]-camera.x,   edges[i][1][1]-camera.y),
				(edges[i-1][1][0]-camera.x, edges[i-1][1][1]-camera.y),
				(edges[i-1][0][0]-camera.x, edges[i-1][0][1]-camera.y),
			),
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
---
Camera: {}
""".format(
				inputs.inputs,
				framerate,
				wait,
				rate,
				delay,
				camera
			),
			font = ("Consolas", 11, ""),
			fill = "white",
			anchor = "nw",
			tag = ("frame", "debug")
		)

	canvas.after(delay,	update)

update()
tk.mainloop()
