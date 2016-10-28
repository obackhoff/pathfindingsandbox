class Node():
	x = 0
	y = 0
	walkable = False
	gCost = 0
	hCost = 0
	cell = None
	parent = None

	def __init__(self, cell, walkable, x, y):
		self.x = x
		self.y = y
		self.walkable = walkable
		self.cell = cell


	def fCost(self):
		return self.gCost + self.hCost

	def setParent(self, node):
		self.parent = node

	def getParent(self):
		return self.parent
