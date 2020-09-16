from tkinter import *
from PIL import Image, ImageTk
class Puzzle:
	def __init__(self, image, imageTk, x, y):
		self.image = image
		self.imageTk = imageTk
		self.pzl_x = x
		self.pzl_y = y
		self.label = Label(image = imageTk)
		self.x = 0
		self.y = 0
		self.size_x, self.size_y = image.size
		self.connected = [self]