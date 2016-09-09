import board
import views
import random
import exceptions

class BoardController:

	def __init__(self):
		sizeGet = False
		while not sizeGet:
			size = input("Please enter the board size( 10-20 ): ")
			sizeGet = True
			try:
				size = int(size)
			except ValueError as e:
				print("Invalid input type, please enter a digital number.")
				sizeGet = False

		colorId = 0
		while colorId == 0:
			color = input("Please enter the piece color( black or white ): ")
			color = color.strip()
			colorGet = True
			if color == 'white':
				colorId = 1
			elif color == 'black':
				colorId = 2
			else:
				print("Invalid color, please reenter the color 'black' or 'white'.")
		
		self.playerColor = colorId
		self.AIColor = 1 if colorId == 2 else 2
		self.boardSize = size
		self.board = board.Board(size = size, color = colorId)
		self.view = views.BoardView(self.board)
		self.playerTrace = []
		self.aiTrace = []

	def start(self):
		winner = 0
		while winner == 0:
			currentColor = self.board.currentColor()
			self.view.displayBoard()
			if currentColor == self.AIColor:
				aiPlayed = False
				while not aiPlayed:
					aiRow = random.randint(0, self.board.size - 1)
					aiCol = random.randint(0, self.board.size - 1)
					aiPlayed = self.board.locationAvailabel((aiRow, aiCol))
					if aiPlayed:
						self.board.update((aiRow, aiCol), self.AIColor)
						self.aiTrace.append((aiRow, aiCol))
			else :
				commandParsed = False
				while not commandParsed:
					yourColor = 'white' if self.playerColor == 1  else 'black'
					command = input("Your next operation"+"( Your color is "+yourColor+" )"+": ")
					command = command.strip()
					if command == 'help':
						self.printHelp()
					elif command == 'exit':
						print('exit!')
						exit(0)
					elif command == 'restart':
						self.restart()
						commandParsed = True
					elif command == 'regret':
						self.regret()
						commandParsed = True
					elif len(command.split(' ')) == 2:
						location = command.split(' ')
						row = location[0]
						col = location[1]
						locationParsed = True
						try:
							row = int(row)
							col = int(col)
						except ValueError as e:
							print("Invalid location format.")
							locationParsed = False
						locationValid = True
						try:
							self.board.update((row - 1, col - 1), self.playerColor)
						except exceptions.OccupiedException as e:
							print('The location you specify is already occupied.')
							locationValid = False
						except exceptions.OutOfRangeException as e:
							print('The location you specify is out of the board range.')
							locationValid = False
						if locationValid:
							self.playerTrace.append((row - 1, col - 1))
							commandParsed = True
					else:
						print('Invalid command.')
			draw = self.board.checkDraw()
			if draw:
				print('Draw!')
				exit(0)
			winner = self.board.winner()
			if winner == self.playerColor:
				print('You win!')
				exit(0)
			elif winner == self.AIColor:
				print('You lose!')
				exit(0)


	def printHelp(self):
		print('command: \'regret\',  usage: roll back to the previous board state.')
		print('command: \'rowID colID\', usage: location at the rowID th row and colID th column.')
		print('command: \'restart\', usage: start a new game.')
		print('command: \'exit\', usage: quite the game.')

	def regret(self):
		if len(self.playerTrace) == 0:
			print('You have no trace to regret.')
		else:
			playerLocation = self.playerTrace.pop()
			aiLocation = self.aiTrace.pop()
			self.board.update(playerLocation, 0)
			self.board.update(aiLocation, 0)

	def restart(self):
		self.board = board.Board(size = self.boardSize, color = self.playerColor)
		self.view = views.BoardView(self.board)
		self.playerTrace = []
		self.aiTrace = []
		self.start()

