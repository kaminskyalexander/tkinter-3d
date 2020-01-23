import tkinter as tk
from binascii import hexlify, unhexlify, crc32
from zlib import decompress

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

class SRGB:
    def __init__(self, red, green, blue):
        self.r = hex(int(red, 16))
        self.g = hex(int(green, 16))
        self.b = hex(int(blue, 16))

    def get(self): return self.r, self.g, self.b


filename = "test.png"
with open(filename, "rb") as f:
    content = f.read()

hexString = hexlify(content)
hexList = [hexString[i:i+2] for i in range(0, len(hexString), 2)]

#signature = hexList[:8]
signature =  [int(i, 16) for i in hexList[:8]]
hexList = hexList[8:]

if(signature == PNG_SIGNATURE):
    while(hexList):
        chunkSize = int(b"".join(hexList[:4]), 16)
        hexList = hexList[4:]
        chunk = hexList[:8 + chunkSize]
        hexList = hexList[8 + chunkSize:]
        chunkType = unhexlify(b"".join(chunk[:4]))
        if(int(b"".join(chunk[chunkSize + 4:]), 16) == crc32(unhexlify(b"".join(chunk[:chunkSize + 4])))):
            if(b"IHDR" == chunkType):
                header = {
                    "width": int(b"".join(chunk[4:8]), 16),
                    "height":int(b"".join(chunk[8:12]), 16),
                    "bit-depth": int(chunk[12], 16),
                    "colour-type":int(chunk[13], 16),
                    "compression":int(chunk[14], 16),
                    "filter": int(chunk[15], 16),
                    "interlace": int(chunk[16], 16)
                }
                print("IHDR Sucess")
            elif(b"PLTE" == chunkType):
                raise NotImplementedError()
            elif(b"IDAT" == chunkType):
                print(header["colour-type"])
                
                if(header["interlace"] != 0): raise NotImplementedError()
                contentString = hexlify(decompress(unhexlify(b"".join(chunk[4:chunkSize+4]))))
                contentList = [contentString[i:i+2] for i in range(0, len(contentString), 2)]
                imageContents = []
                if(header["colour-type"] == 2):
                    for i in range(header["height"]):
                        imageContents.append([])
                        for j in range(header["width"]):
                            imageContents[i].append(
                                SRGB(
                                    contentList[j * 3 + 1 + i + i * header["width"] * 3],
                                    contentList[j * 3 + 2 + i + i * header["width"] * 3],
                                    contentList[j * 3 + 3 + i + i * header["width"] * 3]
                                )
                            )
                
                print(contentList)
                for row in imageContents:
                    for item in row:
                        print(item.get())
                
            elif(b"IEND" == chunkType):
                print("Reached IEND")
                break
            elif(b"tRNS" == chunkType):
                pass
            elif(b"gAMA" == chunkType):
                gamma = float(int(b"".join(chunk[4:8]), 16)) / 100000
                print("Set gamma to:", gamma)
            elif(b"cHRM" == chunkType):
                pass
            elif(b"sRGB" == chunkType):
                renderingIndent = int(chunk[4], 16)
                print("sRGB rendering indent:", renderingIndent)
            elif(b"iCCP" == chunkType):
                pass
            elif(b"iTXt" == chunkType):
                pass
            elif(b"tEXt" == chunkType):
                pass
            elif(b"zTXt" == chunkType):
                pass
            elif(b"bKGB" == chunkType):
                pass
            elif(b"pHYs" == chunkType):
                print("Found Physical Dimensions, Ignoring...")
            elif(b"sBIT" == chunkType):
                pass
            elif(b"sPLT" == chunkType):
                pass
            elif(b"hIST" == chunkType):
                pass
            elif(b"tIME" == chunkType):
                pass
            else:
                print("Invalid chunk type")
        else:
            raise Exception("Invalid CRC (Corrupt PNG?)")
            
    
    
else:
    print("Not a PNG")

tk.mainloop()
