from binascii import hexlify, unhexlify, crc32
from zlib import decompress

# PNG Magic Number
signature = ["0x89", "0x50", "0x4e", "0x47", "0x0d", "0x0a", "0x1a", "0x0a"]

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
		self.pixels = []

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

			# Convert the image data into an array of pixels/colours.
			# Allowed combinations of bit depth and colour type:
		   
			# Colour:   Bit Depths:        Interpretation per pixel:
			# 0 ....... 1, 2, 4, 8, 16 ... A grayscale sample.
			# 2 ....... 8, 16 ............ An R, G, B triple.
			# 3 ....... 1, 2, 4, 8 ....... A palette index; a PLTE chunk must appear.
			# 4 ....... 8, 16 ............ A grayscale sample, followed by an alpha sample.				
			# 6 ....... 8, 16 ............ An R, G ,B triple, followed by an alpha sample.	
			
			#print(self.properties)
			if(self.properties["filter"] == 0):
				# Scanlines (left to right, top to bottom)
				if(self.properties["interlace"] == 0):

					# Data amount per pixel based on specification above
					if   (self.properties["colour-type"] == 0): valuesPerPixel = 1
					elif (self.properties["colour-type"] == 2): valuesPerPixel = 3
					elif (self.properties["colour-type"] == 3): valuesPerPixel = 1
					elif (self.properties["colour-type"] == 4): valuesPerPixel = 2
					elif (self.properties["colour-type"] == 6): valuesPerPixel = 4
					else: raise Exception("Invalid colour type in PNG data")

					# Only allow 8 bit sample depth
					# TODO: Allow for other bit depths
					if(self.properties["bit-depth"] != 8): raise NotImplementedError()

					# Parse data into a 2D list
					data = []
					bytesPerRow = self.properties["width"] * valuesPerPixel + 1
					for y in range(self.properties["height"]):
						data.append([])
						for x in range(bytesPerRow):
							data[y].append(self.data[bytesPerRow * y + x])
						#print(data[y])

					# Unfilter the data
					unfiltered = []
					for y, row in enumerate(data):
						unfiltered.append([])
						filterType = int(row[0], 16)
						for x, byte in enumerate(row[1:]):

							# No filter
							if(filterType == 0):
								pass

							# Sub filter
							elif(filterType == 1):
								
								# Get corresponding byte
								if(x < valuesPerPixel): correspondingByte = 0
								else: correspondingByte = int(unfiltered[y][x - valuesPerPixel], 16)

								# Apply the difference and multiply by power of bit depth
								byte = hexadecimal((correspondingByte + int(byte, 16))%(2**8))

							elif(filterType == 2): raise NotImplementedError()
							elif(filterType == 3): raise NotImplementedError()
							elif(filterType == 4): raise NotImplementedError()
							else:
								raise Exception("Invalid PNG filter type: " + str(filterType))

							unfiltered[y].append(byte)
						#print(unfiltered[y])

					# Convert unfiltered data to pixel colour objects
					for y, row in enumerate(unfiltered):
						self.pixels.append([])
						for x, byte in enumerate(row):
							if(x % valuesPerPixel == 0):

								if(self.properties["colour-type"] == 0):
									shade = byte
									colour = Colour(shade, shade, shade)
								elif(self.properties["colour-type"] == 2):
									r, g, b = unfiltered[y][x:x+3]
									colour = Colour(r, g, b)
								elif(self.properties["colour-type"] == 3):
									raise NotImplementedError()
								elif(self.properties["colour-type"] == 4):
									shade, a = unfiltered[y][x:x+2]
									colour = Colour(shade, shade, shade, alpha = a)
								elif(self.properties["colour-type"] == 6):
									r, g, b, a = unfiltered[y][x:x+4]
									colour = Colour(r, g, b, alpha = a)
								else:
									raise Exception("Invalid colour type (caught too late?)")

								self.pixels[y].append(colour)
						
				# Adam7 Algorithm (Not Implemented)
				elif(self.properties["interlace"] == 1):
					raise NotImplementedError()
				else:
					raise Exception("Unexpected interlacing method")
			else:
				raise Exception("Unexpected PNG filter method")

		else:
			raise IOError("File specified is not a PNG")

		print("Done!")
		for scanline in self.pixels:
			print([pixel.get() for pixel in scanline])

image = PNG("test.png")
#image2 = PNG("test2.png")