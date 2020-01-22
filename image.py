from binascii import hexlify, unhexlify, crc32
from zlib import decompress

# PNG magic number
magicNumber = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]

class Colour:
    def __init__(self, red, green, blue, alpha = 0xff):
        self.r = red
        self.g = green
        self.b = blue
        self.a = alpha

    def get(self): return self.r, self.g, self.b, self.a

class Image:
    def __init__(self, file):
        # Open the file and convert it to a list of hex values
        with open(file, "rb") as f:
            content = hexlify(f.read())
        data = [int(content[i:i+2], 16) for i in range(0, len(content), 2)]
        signature = data[:8]
        data = data[8:]
        if(signature == magicNumber):
            while(data):
                chunk = {
                    "size": sum(data[:4])
                }
        else:
            raise IOError("File specified is not a PNG")

print(magicNumber)
image = Image("test.png")