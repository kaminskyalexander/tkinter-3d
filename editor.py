from game.editor.setup import *
from game.editor.main import Editor

editor = Editor()
debug = True

# Main loop function
def update():

	# Get start time of loop
	start = int(time() * 1000)

	# Clear all frame elements drawn last frame
	canvas.delete("frame")
	
	# Refresh inputs and update the editor
	editor.inputs.refresh()
	editor.update()

	# Get the total time the frame took to compute
	wait = int(time() * 1000) - start
	rate = 1000 // framerate

	# Remove the time from the maximum framerate
	delay = rate - wait if rate - wait < rate else rate
	if(delay < 1): delay = 1

	# Show debug information in top-left of screen
	if(debug):
		canvas.create_text(
			10, 10,
			text = debugTemplate.format(
				editor.inputs.inputs,
				framerate,
				wait,
				rate,
				delay,
				editor.camera
			),
			font = ("Consolas", 11, ""),
			fill = "white",
			anchor = "nw",
			tag = ("frame", "debug")
		)

	# Restart the loop
	canvas.after(delay,	update)

# Initiate the loop
update()

# Tkinter window loop function
tk.mainloop()