from setup import *
from inputs import *

# TODO: Fix for negative values
# This also flips the y value when converting from 3d to 2d space.
def flatten(x, y, z):
	y *= -1
	return x/z, y/z

# We should move this function later, **not to setup**.
def pointToPixel(point):

	# Get the size of the window
	root.update()
	width = canvas.winfo_width()
	height = canvas.winfo_height()

	# Get the coordinates in pixels based on the window width and height
	# This should let the window be stretchable
	x = (width/2)  + (width/2)  * point[0]
	y = (height/2) + (height/2) * point[1]

	return x, y

events = Inputs()

print(flatten(5, 5, 1))

def update():
	canvas.delete("frame")

	x = canvas.create_polygon(
		pointToPixel(flatten(-0.5, -0.5, 1)),
		pointToPixel(flatten( 0.5, -0.5, 1)),
		pointToPixel(flatten( 0.5, -0.5, 2)),
		pointToPixel(flatten(-0.5, -0.5, 2)),
		fill = "gray",
		outline = "#0f0",
		width = 3,
		tag = "frame"
	)

	events.update()
	canvas.after(20, update)

update()
tk.mainloop()
