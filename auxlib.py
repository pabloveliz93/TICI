from random import randint
from time import sleep
class Principal:
	def __init__(self):
		self.vol = 0
		self.temp = 0
		self.flux = 0
	def principal_loop(self):
		self.vol = randint(0, 100)
		self.temp = randint(-50, 50)
		self.flux = randint(0, 100)
		print(self.vol)
		sleep(0.1)