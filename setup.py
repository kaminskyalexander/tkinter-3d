import tkinter as tk
from math import cos, sin, pi
from time import time, sleep
from vector import Vector

root = tk.Tk()
width = 1280
height = 720
framerate = 60
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