import tkinter as tk
from math import cos, sin, atan2, pi

root = tk.Tk()
canvas = tk.Canvas(width = 500, height = 500, bg = "#111", highlightthickness = 0)
canvas.pack()

lines = [
	[(0, 0), (   0, -100)], # N
	[(0, 0), ( 100,    0)], # E
	[(0, 0), (   0,  100)], # S
	[(0, 0), (-100,    0)]  # W
]

def findLineAngle(line):
	x1, y1 = line[0]
	x2, y2 = line[1]

	dy = y2 - y1
	dx = x2 - x1

	theta = atan2(dy, dx)
	theta *= 180/pi

	return theta

def rotateLine(line, degrees):
	angle = degrees*pi/180

	x1, y1 = line[0]
	x2, y2 = line[1]

	mx = (x1 + x2) / 2
	my = (y1 + y2) / 2

	# Use a rotation matrix, centering the point to (0, 0)
	rotated = (
		(
			(cos(angle) * (x1-mx) - sin(angle) * (y1-my)) + mx,
			(sin(angle) * (x1-mx) + cos(angle) * (y1-my)) + my
		),
		(
			(cos(angle) * (x2-mx) - sin(angle) * (y2-my)) + mx,
			(sin(angle) * (x2-mx) + cos(angle) * (y2-my)) + my
		)
	)

	return rotated

angle = 0
def update():
	global angle
	angle += 1
	canvas.delete("all")

	for i, line in enumerate(lines):
		rotated = rotateLine(line, angle)
		canvas.create_line(
			rotated[0][0] + 250, rotated[0][1] + 250,
			rotated[1][0] + 250, rotated[1][1] + 250,
			fill = "#0f0"
		)
		canvas.create_oval(
			rotated[0][0] + 240, rotated[0][1] + 240,
			rotated[0][0] + 260, rotated[0][1] + 260,
			fill = "#0ff"
		)

	canvas.after(20, update)


update()

tk.mainloop()