class InputListener:

	def __init__(self, root):

		self.inputs = {
			"motion": (0, 0),
			"buttons": [],
			"keys": []
		}

		self.queue = []
		root.bind("<KeyPress>", lambda event: self.queue.append(event))
		root.bind("<KeyRelease>", lambda event: self.queue.append(event))
		root.bind("<ButtonPress>", lambda event: self.queue.append(event))
		root.bind("<ButtonRelease>", lambda event: self.queue.append(event))
		root.bind("<Motion>", lambda event: self.queue.append(event))

	def refresh(self):

		for key in self.inputs["keys"]:
			if(key[1] == "release"):
				self.inputs["keys"].remove(key)

		for button in self.inputs["buttons"]:
			if(button[1] == "release"):
				self.inputs["buttons"].remove(button)

		for event in self.queue:
			# Key Press
			if(event.type == "2"):
				self.inputs["keys"].append((event.keycode, "press")) if (event.keycode, "press") not in self.inputs["keys"] else None
			# Key Release
			if(event.type == "3"):
				self.inputs["keys"].remove((event.keycode, "press")) if (event.keycode, "press") in self.inputs["keys"] else None
				self.inputs["keys"].append((event.keycode, "release"))
			# Mouse Button Press
			if(event.type == "4"):
				self.inputs["buttons"].append((event.num, "press")) if (event.num, "press") not in self.inputs["buttons"] else None
			# Mouse Button Release
			if(event.type == "5"):
				self.inputs["buttons"].remove((event.num, "press")) if (event.num, "press") in self.inputs["buttons"] else None
				self.inputs["buttons"].append((event.num, "release"))
			# Motion
			if(event.type == "6"):
				self.inputs["motion"] = event.x, event.y
		
		self.queue.clear()

	def key(self, keycode, state):
		if((keycode, state) in self.inputs["keys"]):
			return True
		return False