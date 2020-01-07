import tkinter as tk
root = tk.Tk()
width = 1280
height = 720
canvas = tk.Canvas(
    root,
    width = width,
    height = height,
    bg = "#000",
    highlightthickness = 0
)
canvas.pack(fill = "both", expand = True)

binds = {
    "forward": 87,
    "left": 65,
    "back": 83,
    "right": 68
}

inputs = {
    "motion": {"x": 0, "y": 0},
    "buttons": [],
    "keys": []
}