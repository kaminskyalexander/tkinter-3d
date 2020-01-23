from binascii import hexlify, unhexlify, crc32
from zlib import decompress

# Takes an integer and converts it to a hexadecimal value
# This value can be converted back to an integer using "int(n, 16)"
def hexadecimal(number):
	# Format method magic
	return "{0:#0{1}x}".format(number, 4)

def hexJoin(*args):
	joined = "0x"
	for arg in args:
		joined += arg[2:]
	return joined

def hexString(*args):
	string = b""
	for arg in args:
		string += unhexlify(arg[2:])
	return string

# PNG Magic Number
signature = ["0x89", "0x50", "0x4e", "0x47", "0x0d", "0x0a", "0x1a", "0x0a"]

class Colour:

	def __init__(self, red, green, blue, alpha = "0xff"):
		self.r = red
		self.g = green
		self.b = blue
		self.a = alpha

	def get(self):
		return self.r, self.g, self.b, self.a

class PNG:

	# See PNG file structure information (PNG specification):
	# http://www.libpng.org/pub/png/spec/1.2/PNG-Contents.html
	def __init__(self, file):

		self.properties = {
			# IHDR Values............
			"width":            None,
			"height":           None,
			"bit-depth":        None,
			"colour-type":      None,
			"compression":      None,
			"filter":           None,
			"interlace":        None,
			# Optional Values........
			"gamma:":           None,
			"rendering-indent": None
		}
		self.data = []

		# Open the file and convert it to a list of hex values
		with open(file, "rb") as f:
			content = hexlify(f.read())
		data = [hexadecimal(int(content[i:i+2], 16)) for i in range(0, len(content), 2)]

		header = data[:8]
		data = data[8:]
		# Signature verification (make sure this file is a PNG)
		if(header == signature):
			while(data):

				# Extract chunk information
				chunkSize = int(hexJoin(*data[:4]), 16)
				chunkType = hexString(*data[4:8])
				chunkData = data[8:chunkSize+8]
				chunkCRC  = int(hexJoin(*data[chunkSize+8:chunkSize+12]), 16)

				# Verify CRC integrity (corruption check)
				if(crc32(hexString(*data[4:chunkSize+8])) == chunkCRC):
					
					# Image header chunk (all crutial image data)
					if(chunkType == b"IHDR"):
						self.properties["width"]       = int(hexJoin(*chunkData[0:4]), 16)
						self.properties["height"]      = int(hexJoin(*chunkData[4:8]), 16)
						self.properties["bit-depth"]   = int(chunkData[8], 16)
						self.properties["colour-type"] = int(chunkData[9], 16)
						self.properties["compression"] = int(chunkData[10], 16)
						self.properties["filter"]      = int(chunkData[11], 16)
						self.properties["interlace"]   = int(chunkData[12], 16)

					# Palette indexes (not implemented)
					elif(chunkType == b"PLTE"):
						raise NotImplementedError()

					# Image data (pixel information)
					elif(chunkType == b"IDAT"):
						# Decompress/unzip the IDAT contents
						imageContent = hexlify(decompress(hexString(*chunkData)))
						# Since there can be multiple IDAT chunks in one PNG file, we can
						# append this information to "self.data" and deal with it later...
						for i in range(0, len(imageContent), 2):
							self.data.append(
								hexadecimal(int(imageContent[i:i+2], 16))
							)

					# End of file
					elif(chunkType == b"IEND"):
						print("Reached end of file.")
						break

					elif(chunkType == b"tRNS"):
						pass
					elif(chunkType == b"gAMA"):
						self.properties["gamma"] = float(int(b"".join(chunkData[:4]), 16)) / 100000
					elif(chunkType == b"cHRM"):
						pass
					elif(chunkType == b"sRGB"):
						self.properties["rendering-indent"] = int(chunkData[0], 16)
					elif(chunkType == b"iCCP"):
						...
					elif(chunkType == b"iTXt"):
						...
					elif(chunkType == b"tEXt"):
						...
					elif(chunkType == b"zTXt"):
						...
					elif(chunkType == b"bKGB"):
						...
					elif(chunkType == b"pHYs"):
						...
					elif(chunkType == b"sBIT"):
						...
					elif(chunkType == b"sPLT"):
						...
					elif(chunkType == b"hIST"):
						...
					elif(chunkType == b"tIME"):
						...
					else:
						raise Exception("Unexpected PNG chunk type")
				else:
					raise Exception("CRC checksum error")

				# Remove chunk from main list
				data = data[chunkSize + 12:]

			# Convert the image data into an array of pixels/colours
			...

		else:
			raise IOError("File specified is not a PNG")

image = PNG("test.png")