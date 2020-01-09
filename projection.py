from setup import *
from inputs import *
from geometry import polygon

events = Inputs()

def update():
	if((binds["forward"], "press") in inputs["keys"]):
		camera.z += 0.05
	if((binds["back"], "press") in inputs["keys"]):
		camera.z -= 0.05
	if((binds["right"], "press") in inputs["keys"]):
		camera.x += 0.05
	if((binds["left"], "press") in inputs["keys"]):
		camera.x -= 0.05

	canvas.delete("frame")
	for i in range(1, 100):
		polygon(
			Vector(-0.5, -0.5, i),
			Vector( 0.5, -0.5, i),
			Vector( 0.5, -0.5, i + 1),
			Vector(-0.5, -0.5, i + 1),
			fill = "gray" if i % 2 == 0 else "lightgray",
			tag = "frame"
		)

	events.update()
	canvas.after(20, update)

update()
tk.mainloop()
