import tkinter as tk
import tkinter.messagebox as popup
from time import time, sleep
from math import pi, cos, sin, atan
from json import loads, dumps
from core.vector import Vector

root = tk.Tk()
width = 1280
height = 720
framerate = 30

canvas = tk.Canvas(
    root,
    width = width,
    height = height,
    bg = "#000",
    highlightthickness = 0
)
canvas.pack(fill = "both", expand = True)

binds = {}

debugTemplate = """\
Racetrack Editor / Test
Inputs: {}
Limit: {}
Wait: {}
Rate: {}
Delay: {}
Camera: {}
"""
