import time

class Maxwell:

	def __init__(self):
		self.sleeping = False
		self.intelligence = 0

	def isAsleep(self, function):
		def wrapper(self):
			if not self.sleeping:
				function()
		return wrapper

	@isAsleep
	def upgrade(self):
		self.intelligence += 1

human = Maxwell()

time.sleep(1) # Some other code...

# Is there a function that gets called before upgrade() is called
human.upgrade()

human.sleeping = True

# This to not call/ get ignored
human.upgrade()

print(human.intelligence)

# def my_decorator(func):
#     def wrapper():
#         print("Something is happening before the function is called.")
#         func()
#         print("Something is happening after the function is called.")
#     return wrapper

# @my_decorator
# def say_whee():
#     print("Whee!")