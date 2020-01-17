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

binds = {
    # Movement.......
    "forward": 87,
    "backward": 83,
    "up": 32,
    "down": 17,
    "speed": 16,
    "left": 81,
    "right": 69,
    # Camera.........
    "look-left": 65,
    "look-right": 68,
    "look-up": 38,
    "look-down": 40,
    "tilt-left": 37,
    "tilt-right": 39,
    # Gameplay.......
    "reset": 82,
    # Debug Camera Offset
    "camoffset-left": 70,
    "camoffset-right": 72,
    "camoffset-up": 84,
    "camoffset-down": 71
}

inputs = {
    "motion": {"x": 0, "y": 0},
    "buttons": [],
    "keys": []
}