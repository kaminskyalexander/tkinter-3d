import tkinter as tk
from binascii import hexlify

PNG_SIGNATURE = [137, 80, 78, 71, 13, 10, 26, 10]

root = tk.Tk()
width = 400
height = 400

canvas = tk.Canvas(
    root,
    width = width,
    height = height,
    bg = "#000",
    highlightthickness = 0
)
canvas.pack(fill = "both", expand = True)


filename = "test.png"
with open(filename, "rb") as f:
    content = f.read()

hexString = hexlify(content)
hexList = [hexString[i:i+2] for i in range(0, len(hexString), 2)]

#signature = hexList[:8]
signature =  [int(i, 16) for i in hexList[:8]]
hexList = hexList[8:]

if(signature == PNG_SIGNATURE):
    chunk = hexList[:4]
    chunkSize = int(b''.join(chunk), 16)
    
    hexList = hexList[4 + chunkSize:]
else:
    print("Not a PNG")

tk.mainloop()