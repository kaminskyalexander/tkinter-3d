from game.setup import *
from core.inputs import InputListener
from game.geometry import polygon, rotate, flip, rotationMatrix

inputs = InputListener(root)
debug = True

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
     
	if inputs.key(*binds["look-up"]):       rotation.x -= 1
	if inputs.key(*binds["look-down"]):     rotation.x += 1
	if inputs.key(*binds["look-left"]):     rotation.y -= 1
	if inputs.key(*binds["look-right"]):    rotation.y += 1
	if inputs.key(*binds["tilt-left"]):     rotation.z += 1
	if inputs.key(*binds["tilt-right"]):    rotation.z -= 1
		
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

	#makeshift fix :)
	if(camera.z > 34):
		camera.z = 0

	canvas.delete("frame")
	# background
	canvas.create_rectangle(
		0, 0, canvas.winfo_width(), canvas.winfo_height(),
		fill = "lightblue",
		width = 0,
		tag = "frame"
	)
	for i in range(0, 100):
		polygon(
			camera, rotation,
			Vector(-0.65, -0.5, (i)/2),
			Vector(-0.45, -0.5, (i)/2),
			Vector(-0.45, -0.5, (i+1)/2),
			Vector(-0.65, -0.5, (i+1)/2),
			fill = "darkred" if i % 2 == 0 else "#ddd"
		)
		polygon(
			camera, rotation,
			Vector( 0.45, -0.5, (i)/2),
			Vector( 0.65, -0.5, (i)/2),
			Vector( 0.65, -0.5, (i+1)/2),
			Vector( 0.45, -0.5, (i+1)/2),
			fill = "darkred" if i % 2 == 0 else "#ddd"
		)
	for i in range(0, 50):
		polygon(
			camera, rotation,
			Vector(-0.5, -0.5, i),
			Vector( 0.5, -0.5, i),
			Vector( 0.5, -0.5, i + 1),
			Vector(-0.5, -0.5, i + 1),
			fill = "#666" if i % 2 == 0 else "#555"
		)
		polygon(
			camera, rotation,
			Vector(-0.6, -0.5, i),
			Vector( -200, -0.5, i),
			Vector( -200, -0.5, i + 1),
			Vector(-0.6, -0.5, i + 1),
			fill = "green" if i % 2 == 0 else "darkgreen"
		)
		polygon(
			camera, rotation,
			Vector(0.6, -0.5, i),
			Vector( 200, -0.5, i),
			Vector( 200, -0.5, i + 1),
			Vector(0.6, -0.5, i + 1),
			fill = "green" if i % 2 == 0 else "darkgreen"
		)

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
			font = ("System", 11, ""),
			anchor = "nw",
			tag = ("frame", "debug")
		)

	canvas.after(delay,	update)

update()
tk.mainloop()
