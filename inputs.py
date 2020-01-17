from setup import root

binds = {
    # Movement ............
    "forward": 87,
    "backward": 83,
    "up": 32,
    "down": 17,
    "speed": 16,
    "left": 81,
    "right": 69,
    # Camera Direction ....
    "look-left": 65,
    "look-right": 68,
    "look-up": 38,
    "look-down": 40,
    "tilt-left": 37,
    "tilt-right": 39,
    # Camera Offset .......
    "camoffset-left": 70,
    "camoffset-right": 72,
    "camoffset-up": 84,
    "camoffset-down": 71,
    # Gameplay ............
    "reset": 82,
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

    def update(self):
        global inputs

        for key in inputs["keys"]:
            if(key[1] == "release"):
                inputs["keys"].remove(key)

        for button in inputs["buttons"]:
            if(button[1] == "release"):
                inputs["buttons"].remove(button)

        for event in self.events:
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
        
        self.events.clear()