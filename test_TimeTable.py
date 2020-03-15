import tkinter as tk
import tkinter.ttk as ttk

root = tk.Tk()
root.title("Performance Debugger")

# How to create columns with headings
tree = ttk.Treeview(root, columns = ("latest", "average"))
tree.heading("#0", text = "Action")
tree.heading("latest", text = "Latest Time")
tree.heading("average", text = "Average Time")

# How to create rows with titles
x = tree.insert("", 0, None, text="User Input", values=("43ms", "39ms"))
tree.insert("", 1, None, text="Matrix Calculation", values=("54ms", "47ms"))
tree.insert("", 2, None, text="Transformation and Rotation", values=("76ms", "67s"))
tree.insert("", 3, None, text="BSP Sorting", values=("10ms", "12ms"))

tree.pack()

# How to change row values after creation
i = 0
def update():
	global i
	i += 1
	tree.set(x, 0, str(i))
	root.after(50, update)

update()

tk.mainloop()