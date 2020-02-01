import tkinter as tk
from binascii import hexlify
from image import PNG

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

image = PNG("test.png")
instance = None # Global

def update():
	global instance
	image.flip()
	instance = tk.PhotoImage(data = image.repackage(), format = "png").zoom(50)

	canvas.delete("update")
	canvas.create_image(0, 0, image = instance, anchor = "nw", tag = "update")
	
	canvas.after(1000, update)

update()
tk.mainloop()