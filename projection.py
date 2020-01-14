from setup import *
from inputs import *
from geometry import polygon, rotate, flip

events = Inputs()
debug = True

def update():
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
		rotation.y -= 0.1
	if((binds["look-right"], "press") in inputs["keys"]):
		rotation.y += 0.1
	if((binds["look-up"], "press") in inputs["keys"]):
		rotation.x -= 0.1
	if((binds["look-down"], "press") in inputs["keys"]):
		rotation.x += 0.1
	if((binds["tilt-left"], "press") in inputs["keys"]):
		rotation.z += 0.1
	if((binds["tilt-right"], "press") in inputs["keys"]):
		rotation.z -= 0.1
	if((binds["reset"], "press") in inputs["keys"]):
		camera.assign(Vector(0, 0, 0))
		rotation.assign(Vector(0, 0, 0))

	movement = rotate(movement, flip(rotation))
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
	for i in range(0, 100):
		polygon(
			Vector(-0.65, -0.5, (i)/2),
			Vector(-0.45, -0.5, (i)/2),
			Vector(-0.45, -0.5, (i+1)/2),
			Vector(-0.65, -0.5, (i+1)/2),
			fill = "darkred" if i % 2 == 0 else "#ddd",
			tag = "frame"
		)
		polygon(
			Vector( 0.45, -0.5, (i)/2),
			Vector( 0.65, -0.5, (i)/2),
			Vector( 0.65, -0.5, (i+1)/2),
			Vector( 0.45, -0.5, (i+1)/2),
			fill = "darkred" if i % 2 == 0 else "#ddd",
			tag = "frame"
		)
	for i in range(0, 50):
		polygon(
			Vector(-0.5, -0.5, i),
			Vector( 0.5, -0.5, i),
			Vector( 0.5, -0.5, i + 1),
			Vector(-0.5, -0.5, i + 1),
			fill = "#666" if i % 2 == 0 else "#555",
			tag = "frame"
		)
		polygon(
			Vector(-0.6, -0.5, i),
			Vector( -20, -0.5, i),
			Vector( -20, -0.5, i + 1),
			Vector(-0.6, -0.5, i + 1),
			fill = "green" if i % 2 == 0 else "darkgreen",
			tag = "frame"
		)
		polygon(
			Vector(0.6, -0.5, i),
			Vector( 20, -0.5, i),
			Vector( 20, -0.5, i + 1),
			Vector(0.6, -0.5, i + 1),
			fill = "green" if i % 2 == 0 else "darkgreen",
			tag = "frame"
		)
	if(debug):
		canvas.create_text(
			10, 10,
			text = "Tkinter 3D Racetrack Test\nFramerate: {}\nX: {}\nY: {}\nZ: {}".format(
				"Undefined",
				camera.x,
				camera.y,
				camera.z
			),
			font = ("System", 11, ""),
			anchor = "nw",
			tag = "frame"
		)

	events.update()
	canvas.after(20, update)

update()
tk.mainloop()
