import exceptions

class Board:

	#white = 1, black = 2
	def __init__(self, **args):
		size = args.get('size', 15)
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

	def winner(self):
		#  row
		for row in range(self.size):
			for col in range(self.size - 4):
				find = True
				winnerColor = self.model[row][col]
				if winnerColor == 0:
					continue
				for k in range(5):
					if not self.model[row][col+k] == winnerColor:
						find = False
						break
				if find:
					return winnerColor

		#  col			
		for col in range(self.size):
			for row in range(self.size - 4):
				find = True
				winnerColor = self.model[row][col]
				if winnerColor == 0:
					continue
				for k in range(5):
					if not self.model[row+k][col] == winnerColor:
						find = False
						break
				if find:
					return winnerColor

		# right-down
		for diff in range(self.size - 4):
			for row in range(diff, self.size - 4):
				find = True
				winnerColor = self.model[row][row-diff]
				if winnerColor == 0:
					continue
				for k in range(5):
					if not self.model[row + k][row- diff + k] == winnerColor:
						find =False
						break
				if find:
					return winnerColor
			for col in range(diff, self.size-4):
				find = True
				winnerColor = self.model[col - diff][col]
				if winnerColor == 0:
					continue
				for k in range(5):
					if not self.model[col - diff + k][col + k] == winnerColor:
						find = False
						break
				if find:
					return winnerColor

		#  left-down
		for accum in range(4, self.size):
			for row in range(accum + 1 - 4):
				find = True
				winnerColor = self.model[row][accum-row]
				if winnerColor == 0:
					continue
				for k in range(5):
					if not self.model[row + k][accum - row - k] == winnerColor:
						find = False
						break
				if find:
					return winnerColor

		for accum in range(self.size, self.size* 2 - 5):
			for col in range(accum + 1 - self.size , self.size - 4):
				find = True
				winnerColor = self.model[accum - col][col]
				if winnerColor == 0:
					continue
				for k in range(5):
					if not self.model[accum - col - k][col + k] == winnerColor:
						find = False
						break
				if find:
					return winnerColor
		
		return 0



