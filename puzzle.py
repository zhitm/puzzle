class Puzzle:
	def __init__(self, image, x, y):
		self.image = image
		self.pzl_x = x
		self.pzl_y = y
		self.x = 0
		self.y = 0
		self.size_x, self.size_y = image.get_rect().size
		self.connected = [self]
