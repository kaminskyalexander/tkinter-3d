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
        cameraX += 10
    if((binds["left"], "press") in inputs["keys"]):
        cameraX -= 10

    canvas.create_polygon(
    [
        point(-100 + cameraX, -100,  0 - cameraZ),
        point( 100 + cameraX, -100,  0 - cameraZ),
        point( 100 + cameraX,  100, 25 - cameraZ),
        point(-100 + cameraX,  100, 25 - cameraZ)
    ],
    fill = "gray",
    tag = "test"
)
    events.update()
    canvas.after(20, update)

update()
tk.mainloop()
