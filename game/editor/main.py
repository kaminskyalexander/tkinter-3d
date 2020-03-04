from game.editor.setup import *
from core.inputs import InputListener
from core.util import snap, getNeighbours, find2dLineAngle, rotate2dLine, angleAverage

# Racetrack class: Takes care of all the variables related to the world
class Racetrack:

	# Initialize the path
	def __init__(self):
		self.path = []
		self.width = 50

	@property
	def edges(self):
		edges = []
		angles = []
		for i, point in enumerate(self.path):
			before, after = getNeighbours(i, self.path)

			# Find the average angle of the two lines
			angle = angleAverage(find2dLineAngle(before, point), find2dLineAngle(point, after))
			# Make the angle perpendicular to the road
			angle += 90

			edge = rotate2dLine(
				(
					(point.x - self.width, point.y),
					(point.x + self.width, point.y)
				),
				angle
			)

			angles.append(angle)
			edges.append(edge)

		return angles, edges

	# Draw the racetrack
	def draw(self, camera):
		for point in self.path:
			canvas.create_oval(
				point.x - 5 - camera.x, point.y - 5 - camera.y,
				point.x + 5 - camera.x, point.y + 5 - camera.y,
				fill = "red",
				tag = ("frame", "node")
			)

		angles, edges = self.edges
		for i, edge in enumerate(edges):
			canvas.create_polygon(
				edges[i][0][0]-camera.x,   edges[i][0][1]-camera.y,
				edges[i][1][0]-camera.x,   edges[i][1][1]-camera.y,
				edges[i-1][1][0]-camera.x, edges[i-1][1][1]-camera.y,
				edges[i-1][0][0]-camera.x, edges[i-1][0][1]-camera.y,
				fill = "#444" if i%2 == 0 else "#666",
				outline = "lightgray",
				tag = ("frame", "road")
			)
			canvas.create_text(
				edges[i][0][0]-camera.x,   edges[i][0][1]-camera.y,
				text = str(angles[i]),
				font = ("Consolas", 14, ""),
				fill = "#0ff",
				tag = ("frame", "debug")
			)


class Cursor(Vector):

	def __init__(self, x, y):
		self.size = 10
		super().__init__(snap(x, interval = 50), snap(y, interval = 50), 0)

	def draw(self, camera):
		x = snap(self.x + camera.x, interval = 50) - camera.x
		y = snap(self.y + camera.y, interval = 50) - camera.y
		lines = (
			(
				x - self.size, y,
				x + self.size, y
			),
			(
				x, y - self.size,
				x, y + self.size
			)
		)

		for line in lines:
			canvas.create_line(
				*line,
				fill = "white",
				width = 2,
				tag = ("frame", "cursor")
			)

# Editor class: takes care of more general functionality
class Editor:

	def __init__(self):
		self.inputs = InputListener(root)
		self.camera = Vector(0, 0, 0)
		self.world = Racetrack()
		self.cursor = Cursor(0, 0)

	def export(self, filepath = "Track.json"):
		with open(filepath, "w") as f:
			contents = {"points": []}
			# Convert vector to list of points
			for point in self.world.path:
				contents["points"].append((point.x, point.y))
			f.write(dumps(contents))

	def update(self):
		self.world.draw(self.camera)

		# Draw the grid
		size = 50
		width = canvas.winfo_width()
		height = canvas.winfo_height()

		for y in range(int(height/size) + 2):
			for x in range(int(width/size) + 2):
				canvas.create_rectangle(
					(x)*size   - self.camera.x%size, y*size     - self.camera.y%size,
					(x+1)*size - self.camera.x%size, (y+1)*size - self.camera.y%size,
					fill = "",
					outline = "#333",
					tag = ("frame", "grid")
				)

		# Get cursor position
		self.cursor.x = self.inputs.motion[0]
		self.cursor.y = self.inputs.motion[1]
		self.cursor.draw(self.camera)

		# Place vertex
		if self.inputs.button(1, "trigger"):
			self.world.path.append(Vector(
				snap(self.cursor.x + self.camera.x, interval = 50),
				snap(self.cursor.y + self.camera.y, interval = 50),
				0 # Z coordinate
			))

		# R to reset
		if self.inputs.key(82, "trigger"):
			self.world.path = []
			self.camera = Vector(0, 0, 0)

		# Ctrl+Z to undo
		if self.inputs.key(17, "press") and self.inputs.key(90, "trigger"):
			if len(self.world.path) > 1: del self.world.path[-1]

		# Ctrl+E to export level
		if self.inputs.key(17, "press") and self.inputs.key(69, "trigger"):
			self.export()
			popup.showinfo("Export", "Exported to file level.json")

		if self.inputs.key(87, "press"): self.camera.y -= 10 # W: Up
		if self.inputs.key(65, "press"): self.camera.x -= 10 # A: Left
		if self.inputs.key(83, "press"): self.camera.y += 10 # S: Down
		if self.inputs.key(68, "press"): self.camera.x += 10 # D: Right

		canvas.tag_raise("road")
		canvas.tag_raise("node")
		canvas.tag_raise("cursor")
		canvas.tag_raise("debug")
