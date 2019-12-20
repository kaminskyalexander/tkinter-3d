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
