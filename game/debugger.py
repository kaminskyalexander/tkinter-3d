from game.setup import tk, ttk

class PerformanceDebugger:

	def __init__(self, root):

		# Create new window
		self.toplevel = tk.Toplevel(root)
		self.toplevel.title("Performance Debugger")

		# Initialize the treeview widget
		self.tree = ttk.Treeview(self.toplevel, columns = ("latest", "average"))

		# Add headings to the columns
		self.tree.heading("#0", text = "Action")
		self.tree.heading("latest", text = "Latest Time")
		self.tree.heading("average", text = "Average Time")

		# Place the widget
		self.tree.pack()

		# Dictionary for storing entries
		self.entries = {}

		# Prevent the window from being closed
		def disable(): pass
		self.toplevel.protocol("WM_DELETE_WINDOW", disable)

	def register(self, action):
		self.entries[action] = {
			"history": [],
			"row": self.tree.insert("", 0, text = action, values = ("???", "???"))
		}

	def record(self, action, time):
		time = round(time * 1000, 3)
		if len(self.entries[action]["history"]) > 100:
			del self.entries[action]["history"][0]
		self.entries[action]["history"].append(time)

	def update(self):
		for key, entry in self.entries.items():
			if len(entry["history"]) > 0:
				latest = entry["history"][-1]
				average = round(sum(entry["history"]) / len(entry["history"]), 3)
				self.tree.set(self.entries[key]["row"], 0, str(latest) + "ms")
				self.tree.set(self.entries[key]["row"], 1, str(average) + "ms")
