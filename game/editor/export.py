from json import dumps

def export(path, dictionary):
	with open(path, "w") as f:
		f.write(dumps(dictionary))