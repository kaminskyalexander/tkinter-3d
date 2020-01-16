from setup import *
from inputs import *
from geometry import polygon, rotate, flip, rotationMatrix

events = Inputs()
debug = True

def update():
	start = int(time() * 1000)

	movement = Vector(0, 0, 0)
	if((binds["forward"], "press") in inputs["keys"]):
		if((binds["speed"], "press") in inputs["keys"]):
			movement.z += 0.3
		else:
			movement.z += 0.1
	if((binds["backward"], "press") in inputs["keys"]):
		movement.z -= 0.1
	if((binds["down"], "press") in inputs["keys"]):
		movement.y -= 0.1
	if((binds["up"], "press") in inputs["keys"]):
		movement.y += 0.1
	if((binds["look-left"], "press") in inputs["keys"]):
		rotation.y -= 1
	if((binds["look-right"], "press") in inputs["keys"]):
		rotation.y += 1
	if((binds["look-up"], "press") in inputs["keys"]):
		rotation.x -= 1
	if((binds["look-down"], "press") in inputs["keys"]):
		rotation.x += 1
	if((binds["tilt-left"], "press") in inputs["keys"]):
		rotation.z += 1
	if((binds["tilt-right"], "press") in inputs["keys"]):
		rotation.z -= 1
	if((binds["reset"], "press") in inputs["keys"]):
		camera.assign(Vector(0, 0, 0))
		rotation.assign(Vector(0, 0, 0))
		offset.assign(Vector(0, 0, 0))
	if((binds["camoffset-up"], "press") in inputs["keys"]):
		offset.y += 5
	if((binds["camoffset-down"], "press") in inputs["keys"]):
		offset.y -= 5
	if((binds["camoffset-left"], "press") in inputs["keys"]):
		offset.x += 5
	if((binds["camoffset-right"], "press") in inputs["keys"]):
		offset.x -= 5

	movement = rotate(movement, rotationMatrix(flip(rotation)))
	camera.add(movement)

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
	# for i in range(0, 100):
	# 	polygon(
	# 		Vector(-0.65, -0.5, (i)/2),
	# 		Vector(-0.45, -0.5, (i)/2),
	# 		Vector(-0.45, -0.5, (i+1)/2),
	# 		Vector(-0.65, -0.5, (i+1)/2),
	# 		fill = "darkred" if i % 2 == 0 else "#ddd"
	# 	)
	# 	polygon(
	# 		Vector( 0.45, -0.5, (i)/2),
	# 		Vector( 0.65, -0.5, (i)/2),
	# 		Vector( 0.65, -0.5, (i+1)/2),
	# 		Vector( 0.45, -0.5, (i+1)/2),
	# 		fill = "darkred" if i % 2 == 0 else "#ddd"
	# 	)
	# for i in range(0, 50):
	# 	polygon(
	# 		Vector(-0.5, -0.5, i),
	# 		Vector( 0.5, -0.5, i),
	# 		Vector( 0.5, -0.5, i + 1),
	# 		Vector(-0.5, -0.5, i + 1),
	# 		fill = "#666" if i % 2 == 0 else "#555"
	# 	)
	# 	polygon(
	# 		Vector(-0.6, -0.5, i),
	# 		Vector( -20, -0.5, i),
	# 		Vector( -20, -0.5, i + 1),
	# 		Vector(-0.6, -0.5, i + 1),
	# 		fill = "green" if i % 2 == 0 else "darkgreen"
	# 	)
	# 	polygon(
	# 		Vector(0.6, -0.5, i),
	# 		Vector( 20, -0.5, i),
	# 		Vector( 20, -0.5, i + 1),
	# 		Vector(0.6, -0.5, i + 1),
	# 		fill = "green" if i % 2 == 0 else "darkgreen"
	# 	)
	polygon(
		Vector(-10, -1, 1),
		Vector( 10, -1, 1),
		Vector( 10, -1, 4),
		Vector(-10, -1, 4),
		debug = True,
		fill = "yellow"
	)

	canvas.tag_raise("debug")
	events.update()
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
			tag = ("frame", debug)
		)

	canvas.after(delay,	update)

update()
tk.mainloop()
