
class BoardView:

	def __init__(self, board):
		self.board = board
		self.size = board.size

	def displayBoard(self):
		self._printAboveLabel()
		for i in range(self.size):
			self._printHorizentalBoundry()
			rowModel = self.board.model[i]
			rowView = ''
			if i < 9:
				rowView = rowView + ' '
			rowView = rowView + str(i + 1) + '|'
			for j in range(len(rowModel)):
				piece = ''
				if rowModel[j] == 1:
					piece = ' ○'
				elif rowModel[j] == 2:
					piece = ' ●'
				else:
					piece = '  '
				piece = piece + ' |'
				rowView = rowView + piece
			print(rowView)
		self._printHorizentalBoundry()

	def _printAboveLabel(self):
		label = ' ' * 3
		for i in range(self.size):
			label = label + ' ' + str(i+1) + ' '
			if i < 9:
				label = label + ' '
		print(label)

	def _printHorizentalBoundry(self):
		line = ' ' * 3
		for i in range(self.size):
			line = line + ' 一 '
		print(line)
	
	