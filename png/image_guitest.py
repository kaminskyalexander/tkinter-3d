import tkinter as tk
from image_wrapper import BetterImage

root = tk.Tk()
width = 400
height = 400
canvas = tk.Canvas(
    root,
    width = width,
    height = height,
    bg = "#000",
    highlightthickness = 0
)
canvas.pack(fill = "both", expand = True)

# Create the image
image = BetterImage("test.png")
x = 5
def update():
	global x
	image.resize(x, x)
	x+= 1
	canvas.delete("update")
	canvas.create_image(0, 0, image = image.instance, anchor = "nw", tag = "update")
	canvas.after(20, update)
update()
tk.mainloop()