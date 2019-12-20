import tkinter as tk

root = tk.Tk()

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

class Inputs:

    def __init__(self):
        self.events = []

        root.bind(
            "<KeyPress>",
            lambda event: (
                self.events.append(event)
            )
        )
        root.bind(
            "<KeyRelease>",
            lambda event: (
                self.events.append(event)
            )
        )
        root.bind(
            "<ButtonPress>",
            lambda event: (
                self.events.append(event)
            )
        )
        root.bind(
            "<ButtonRelease>",
            lambda event: (
                self.events.append(event)
            )
        )
        root.bind(
            "<Motion>",
            lambda event: (
                self.events.append(event)
            )
        )

    @staticmethod
    def apply(args):
        global inputs
        for key in inputs["keys"]:
            if(key[1] == "release"):
                inputs["keys"].remove(key)

        for button in inputs["buttons"]:
            if(button[1] == "release"):
                inputs["buttons"].remove(button)

        for event in args:
            # Key Press
            if(event.type == "2"):
                inputs["keys"].append((event.keycode, "press")) if (event.keycode, "press") not in inputs["keys"] else None
            # Key Release
            if(event.type == "3"):
                inputs["keys"].remove((event.keycode, "press")) if (event.keycode, "press") in inputs["keys"] else None
                inputs["keys"].append((event.keycode, "release"))
            # Mouse Button Press
            if(event.type == "4"):
                inputs["buttons"].append((event.num, "press")) if (event.num, "press") not in inputs["buttons"] else None
            # Mouse Button Release
            if(event.type == "5"):
                inputs["buttons"].remove((event.num, "press")) if (event.num, "press") in inputs["buttons"] else None
                inputs["buttons"].append((event.num, "release"))
            # Motion
            if(event.type == "6"):
                inputs["motion"]["x"] = event.x
                inputs["motion"]["y"] = event.y

    def update(self):
        Inputs.apply(self.events)
        self.events.clear()

width = 1280
height = 720

canvas = tk.Canvas(
    root,
    width = width,
    height = height,
    bg = "#25bed9",
    highlightthickness = 0
)
canvas.pack()


def point(X, Y, Z):
    Y *= -1
    if(Z):
        if(Z < 0):
            Z = abs(Z/10) + 1
            x = X*Z + width/2
            y = Y*Z + height/2
        elif(Z > 0):
            Z = (Z/10) + 1
            x = X/Z + width/2
            y = Y/Z + height/2
    else:
        x = X + width/2
        y = Y + height/2
    return x, y

seglen = 5
roadw = 800
cameraZ = 0
events = Inputs()

canvas.create_polygon(
    [
        point(-100, -100, 0),
        point(100, -100, 0),
        point(100, 100, 100),
        point(-100, 100, 100)
    ],
    fill = "gray"
)

def update():
    print(inputs)
    events.update()
    canvas.after(20, update)

update()
tk.mainloop()
