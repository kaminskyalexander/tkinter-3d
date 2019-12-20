from setup import *
from inputs import *

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
cameraX = 0
cameraZ = 0
events = Inputs()

def update():

    global cameraX, cameraZ
    canvas.delete("test")

    if((binds["forward"], "press") in inputs["keys"]):
        cameraZ += 1
    if((binds["back"], "press") in inputs["keys"]):
        cameraZ -= 1
    if((binds["right"], "press") in inputs["keys"]):
        cameraX += 20
    if((binds["left"], "press") in inputs["keys"]):
        cameraX -= 20

    for i in range(25):
        canvas.create_polygon(
        [
            point(-roadw/2 - cameraX, -100, seglen * (i    ) - cameraZ),
            point( roadw/2 - cameraX, -100, seglen * (i    ) - cameraZ),
            point( roadw/2 - cameraX, -100, seglen * (i + 1) - cameraZ),
            point(-roadw/2 - cameraX, -100, seglen * (i + 1) - cameraZ)
        ],
        fill = ("gray") if i%2 else ("darkgray"),
        tag = "test"
    )
    events.update()
    canvas.after(20, update)

update()
tk.mainloop()
