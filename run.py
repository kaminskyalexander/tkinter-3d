from game.setup import *
from core.inputs import InputListener
from game.geometry import rotate, flip, rotationMatrix
from game.world import World, Racetrack, Polygon
from game.cube import Cube

inputs = InputListener(root)
debug = True

# with open("Track.json", "r") as f:
# 	world = Racetrack(canvas, loads(f.read()))

# world = Cube()

world = World(
	Polygon(
		canvas,
		Vector(-1, -1, 0),
		Vector( 1, -1, 0),
		Vector( 1,  1, 0),
		Vector(-1,  1, 0),
		fill = "#f0f"
	),
	Polygon(
		canvas,
		Vector(0, -1, -1),
		Vector(0, -1,  1),
		Vector(0,  1,  1),
		Vector(0,  1, -1),
		fill = "#0ff"
	)
)

def update():
	global camera, rotation, offset

	start = int(time() * 1000)

	movement = Vector(0, 0, 0)
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

	if inputs.key(*binds["reset"]):
		camera = Vector(0, 0, 0)
		rotation = Vector(0, 0, 0)
		offset = Vector(0, 0, 0)

	movement = rotate(movement, rotationMatrix(flip(rotation)))
	camera += movement

	canvas.delete("frame")

	matrix = rotationMatrix(rotation)
	world.draw(camera, matrix)

	canvas.tag_raise("debug")
	wait = int(time() * 1000) - start
	rate = 1000 // framerate
	delay = rate - wait if rate - wait < rate else rate
	if(delay < 1): delay = 1

	if(debug):
		canvas.create_text(
			10, 10,
			text = """\
Tkinter 3D Racetrack Test
XYZ: {} / {} / {}
Rotation: {} / {} / {}
Offset: {} / {} / {}
Framerate Info:
   Configured FPS: {}
   Wait: {}
   Rate: {}
   Delay: {}\
""".format(
				camera.x, camera.y, camera.z,
				rotation.x, rotation.y,	rotation.z,
				offset.x, offset.y, offset.z,
				framerate,
				wait,
				rate,
				delay
			),
			font = ("Consolas", 11, ""),
			anchor = "nw",
			tag = ("frame", "debug"),
			fill = "white"
		)

	canvas.after(delay,	update)

update()
tk.mainloop()
