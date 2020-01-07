from setup import root, inputs

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
        root.bind(
            "<Configure>",
            lambda event: (
                root.update()
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