import exceptions

class Board:

	#white = 1, black = 2
	def __init__(self, **args):
		size = args.get('size', 10)
		color = args.get('color', 1)
		self.color = color % 2
		if size > 20:
			print("Board size too large, set to maximum size :20")
			size = 20
		if size < 10:
			print("Board size too small, set to minimun size: 10")
			size = 10
		self.size = size
		self.model = [[0 for i in range(self.size)] for j in range(self.size)]
		self.blackNum = 0
		self.whiteNum = 0

	def update(self, coord, player):
		row = coord[0]
		col = coord[1]
		if row >= self.size or col >= self.size:
			raise exceptions.OutOfRangeException()
		oldValue = self.model[row][col]
		if not oldValue == 0 and player != 0:
			raise exceptions.OccupiedException()
		self.model[row][col] = player
		if player == 1:
			self.whiteNum = self.whiteNum + 1
		elif player == 2:
			self.blackNum = self.blackNum + 1

	def locationAvailabel(self, coord):
		row = coord[0]
		col = coord[1]
		return self.model[row][col] == 0

	def getModel(self):
		return self.model

	def currentColor(self):
		return 1 if self.whiteNum <= self.blackNum else 2

	def playerColor(self):
		return self.color

	def AIColor(self):
		return 1 - self.color

	def checkDraw(self):
		hasEmpty = False
		for row in range(self.size):
			for col in range(self.size):
				if self.model[row][col] == 0:
					hasEmpty = True
		return not hasEmpty

	def emptyBoard(self):
		empty = True
		for row in range(self.size):
			for col in range(self.size):
				if self.model[row][col] != 0:
					empty = False
		return empty

	def winner(self):
		#  row
		for row in range(self.size):
			colorCount = 0
			winnerColor = 0
			for col in range(self.size):
				curColor = self.model[row][col]
				if curColor == 0:
					continue
				if curColor == winnerColor:
					if winnerColor != 0:
						colorCount += 1
				else: 
					winnerColor = curColor
					colorCount = 1
				if colorCount == 5:
					return winnerColor

		#  col			
		for col in range(self.size):
			winnerColor = 0
			colorCount = 0
			for row in range(self.size):
				curColor = self.model[row][col]
				if curColor == 0:
					continue
				if curColor == winnerColor:
					if winnerColor != 0:
						colorCount += 1
				else: 
					winnerColor = curColor
					colorCount = 1
				if colorCount == 5:
					return winnerColor

		for diff in range(self.size - 4):
			winnerColor = 0
			colorCount = 0
			for row in range(diff, self.size):
				curColor = self.model[row][row-diff]
				if curColor == 0:
					continue
				if curColor == winnerColor:
					if winnerColor != 0:
						colorCount += 1
				else: 
					winnerColor = curColor
					colorCount = 1
				if colorCount == 5:
					return winnerColor

			winnerColor = 0
			colorCount = 0
			for col in range(diff, self.size):
				curColor = self.model[col - diff][col]
				if curColor == 0:
					continue
				if curColor == winnerColor:
					if winnerColor != 0:
						colorCount += 1
				else: 
					winnerColor = curColor
					colorCount = 1
				if colorCount == 5:
					return winnerColor

		
		for accum in range(4, self.size):
			winnerColor = 0
			colorCount = 0
			for row in range(accum + 1):
				curColor = self.model[row][accum-row]
				if curColor == 0:
					continue
				if curColor == winnerColor:
					if winnerColor != 0:
						colorCount += 1
				else: 
					winnerColor = curColor
					colorCount = 1
				if colorCount == 5:
					return winnerColor

		for accum in range(self.size, self.size* 2 - 5):
			winnerColor = 0
			colorCount = 0
			for col in range(accum + 1 - self.size , self.size):
				curColor = self.model[accum - col][col]
				if curColor == 0:
					continue
				if curColor == winnerColor:
					if winnerColor != 0:
						colorCount += 1
				else: 
					winnerColor = curColor
					colorCount = 1
				if colorCount == 5:
					return winnerColor
		
		return 0

	def fork(self):
		newBoard = Board(size = self.size, color = self.color)
		newBoard.blackNum = self.blackNum
		newBoard.whiteNum = self.whiteNum
		newBoard.model = []
		for i in range(self.size):
			newBoard.model.append(self.model[i][0:])
		return newBoard

	def __hash__(self):
		hashcode = 0
		for i in range(self.size):
			for j in range(self.size):
				value = self.model[i][j]
				hashcode = hashcode + i * 100 * value + j * value
		return hashcode

	def __eq__(self, other):
		if self.size != other.size:
			return False
		for i in range(self.size):
			for j in range(self.size):
				if self.model[i][j] != other.model[i][j]:
					return False
		return True

