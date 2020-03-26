import tkinter as tk
import tkinter.ttk as ttk
from math import cos, sin, atan, pi, sqrt
from time import time, sleep
from json import loads
from core.vector import Vector
from game.debugger import PerformanceDebugger

root = tk.Tk()
width = 1280
height = 720
framerate = 30
camera = Vector(0, 0, 0)
rotation = Vector(0, 0, 0)
offset = Vector(0, 0, 0)

canvas = tk.Canvas(
    root,
    width = width,
    height = height,
    bg = "#000",
    highlightthickness = 0
)
canvas.pack(fill = "both", expand = True)

binds = {
	# Modifiers .......................
	"shift": (16, "press"),
	"ctrl": (17, "press"),
	"alt": (18, "press"),
	# Movement ........................
	"forward": (87, "press"),
	"backward": (83, "press"),
	"up": (32, "press"),
	"down": (17, "press"),
	"speed": (16, "press"),
	"left": (81, "press"),
	"right": (69, "press"),
	# Camera Direction ................
	"look-left": (65, "press"),
	"look-right": (68, "press"),
	"look-up": (38, "press"),
	"look-down": (40, "press"),
	"tilt-left": (37, "press"),
	"tilt-right": (39, "press"),
	# Gameplay ........................
	"reset": (82, "press"),
	# Debug ...........................
	"camoffset-left": (70, "press"),
	"camoffset-right": (72, "press"),
	"camoffset-up": (84, "press"),
	"camoffset-down": (71, "press"),
	"performance": (80, "trigger")
}

debug = True
debugger = PerformanceDebugger(root)

# Force show the window
root.focus_force()