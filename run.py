from game.setup import *
from core.inputs import InputListener
from game.geometry import rotate, flip, rotationMatrix
from game.world import World
from game.polygon import Polygon
from game.racetrack import Racetrack
from game.cube import Cube

inputs = InputListener(root)

# with open("Track.json", "r") as f:
# 	world = Racetrack(canvas, loads(f.read()))

world = World(
	Polygon(
		canvas,
		Vector(3, -1, 0),
		Vector(5, -1, 0),
		Vector(5,  1, 0),
		Vector(3,  1, 0),
		fill = "#808080"
	)
)

world.extend(World(
	Polygon(
		canvas,
		Vector(0, -1, -3),
		Vector(0, -1, -5),
		Vector(0,  1, -5),
		Vector(0,  1, -3),
		fill = "#808080"
	)
))

world.extend(World(
	Polygon(
		canvas,
		Vector(-1, 0, 3),
		Vector(-1, 0, 5),
		Vector( 1, 0, 5),
		Vector( 1, 0, 3),
		fill = "#808080"
	)
))

world.extend(Cube())

# world = Cube()

def update():
	global camera, rotation, offset

	debugger.start("Total")
	start = time()

	movement = Vector(0, 0, 0)

	debugger.start("User Input")
	inputs.refresh()

	if inputs.key(*binds["forward"]):
		if inputs.key(*binds["speed"]):
			movement.z += 0.3
		else: movement.z += 0.1
	if inputs.key(*binds["backward"]):    movement.z -= 0.1
	if inputs.key(*binds["left"]):        movement.x -= 0.1
	if inputs.key(*binds["right"]):       movement.x += 0.1
	if inputs.key(*binds["down"]):        movement.y -= 0.1
	if inputs.key(*binds["up"]):          movement.y += 0.1

	if inputs.key(*binds["look-up"]):       rotation.x -= 2
	if inputs.key(*binds["look-down"]):     rotation.x += 2
	if inputs.key(*binds["look-left"]):     rotation.y -= 2
	if inputs.key(*binds["look-right"]):    rotation.y += 2
	if inputs.key(*binds["tilt-left"]):     rotation.z += 2
	if inputs.key(*binds["tilt-right"]):    rotation.z -= 2

	if inputs.key(*binds["camoffset-up"]):    offset.y += 5
	if inputs.key(*binds["camoffset-down"]):  offset.y -= 5
	if inputs.key(*binds["camoffset-left"]):  offset.x += 5
	if inputs.key(*binds["camoffset-right"]): offset.x -= 5

	if inputs.key(*binds["f1"]):      world.drawingMode = 0
	if inputs.key(*binds["f2"]):      world.drawingMode = 1

	if inputs.key(*binds["reset"]):
		camera = Vector(0, 0, 0)
		rotation = Vector(0, 0, 0)
		offset = Vector(0, 0, 0)

	if inputs.key(*binds["performance"]):
		debugger.toggle()

	movement = rotate(movement, rotationMatrix(-rotation))
	camera += movement

	debugger.stop("User Input")

	canvas.delete("frame")

	debugger.start("Matrix Calculation")
	matrix = rotationMatrix(rotation)
	debugger.stop("Matrix Calculation")

	debugger.start("World Drawing")
	world.draw(camera, matrix)
	debugger.stop("World Drawing")
	debugger.stop("Polygon Transformation")
	debugger.stop("Polygon Culling")
	debugger.stop("Polygon Drawing")

	canvas.tag_raise("debug")

	debugger.stop("Total")

	wait = time() * 1000 - start * 1000
	rate = 1000 // framerate
	delay = int(rate - wait if rate - wait < rate else rate)
	if(delay < 1): delay = 1

	if(debug):
		canvas.create_text(
			10, 10,
			text = """\
Tkinter 3D Rendering [{}fps]
F1 for default rendering...
F2 for wireframe rendering...
ALT+P for performance debugging...
XYZ: {} / {} / {}
Rotation: {} / {} / {}
Offset: {} / {} / {}
""".format(
				int(1000/wait),
				*(round(value, 2) for value in camera),
				*(round(value, 2) for value in rotation),
				*(round(value, 2) for value in offset)
			),
			font = ("Consolas", 11, ""),
			anchor = "nw",
			tag = ("frame", "debug"),
			fill = "white"
		)

	debugger.update()

	canvas.after(delay,	update)

update()
tk.mainloop()
