import tkinter as tk
from binascii import hexlify
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

def update():
	image.flip()
	canvas.delete("update")
	canvas.create_image(0, 0, image = image.instance, anchor = "nw", tag = "update")
	canvas.after(1000, update)

update()
tk.mainloop()