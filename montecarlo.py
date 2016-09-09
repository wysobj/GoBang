import board
import datetime
import math
import random

class MonteCarloAI:

	def __init__(self, board, color):
		self.board = board
		self.color = color
		self.move = int(50 * board.size / 10)
		self.timeInterval = datetime.timedelta(seconds = 3)

	def getLocation(self):
		self.plays = {}
		self.wins = {}
		begin = datetime.datetime.utcnow()
		game = 0
		while datetime.datetime.utcnow() - begin < self.timeInterval:
			self.runSimulation()
			game = game + 1
		print("AI runs "+str(game)+" simulations.")
		bestStep = None
		bestProb = 0
		nextSteps = self._getNextSteps(self.board)
		for step in nextSteps:
			nextState = (self._getNextState(self.board, step, self.color), self.color)
			playNum = self.plays.get(nextState, 1)
			winNum = self.wins.get(nextState, 0)
			prob = winNum / playNum
			if prob >= bestProb:
				bestStep = step
				bestProb = prob
		return bestStep

	def runSimulation(self):
		curState = self.board
		visited = set()
		extended = False
		winner = 0
		for i in range(self.move):
			nextSteps = self._getNextSteps(curState)
			curColor = curState.currentColor()
			nextStates = [self._getNextState(curState, step) for step in nextSteps]
			nextState = None
			if all(plays.get((state, curColor)) for state in nextStates):
				logSum = log(sum(self.plays.get((state, curColor)) for state in nextStates))
				bestState = None
				bestUCB = 0
				for state in nextStates:
					playNum = self.plays.get((state, curColor), 1)
					winNum = self.wins.get((state, curColor), 0)
					ucb = winNum / playNum + logSum / playNum
					if ucb >= bestUCB:
						bestState = state
						bestUCB = ucb
				nextState = bestState
			else:
				choice = random.randint(len(nextStates) - 1)
				nextState = nextStates[choice]

			if not extended and (nextState, curColor) not in self.plays:
				self.plays[(nextState, curColor)] = 0
				self.wins[(nextState, curColor)] = 0

			visited.add((nextState, curColor))
			winner = nextState.winner()
			if winner != 0:
				break

		for foo in visited:
			if foo not in self.plays.keys():
				continue
			self.plays[foo] += 1
			if winner == foo[1]:
				self.wins[foo] += 1

	def _getNextSteps(self, curBoard):
		steps = []
		for i in range(self.board.size):
			for j in range(self.board.size):
				if curBoard.model[i][j] > 0:
					continue
				curLocation = (i, j)
				nearByLocations = self._getNearByLocations(curLocation)
				for checkLocation in nearByLocations:
					row = checkLocation[0]
					col = checkLocation[1]
					if curBoard[row][col] > 0:
						steps.append(curLocation)
						break
		return steps

	def _getNearByLocations(self, curLocation):
		neibourRange = 2
		locations = []
		curRow = curLocation[0]
		curCol = curLocation[1]
		boardSize = self.board.size
		above = curRow - neibourRange if curRow > neibourRange else 0
		left = curCol - neibourRange if curCol > neibourRange else 0
		bottom = curRow + neibourRange if curRow + neibourRange <= boardSize else boardSize
		right =  curCol + neibourRange if curCol + neibourRange <= boardSize else boardSize
		for i in range(above, bottom):
			for j in range(left, right):
				locations.append((i, j))
		locations.remove(curLocation)
		return locations

	def _getNextState(self, board, location):
		boardCopy = board.fork()
		color = boardCopy.currentColor()
		boardCopy.update(localtion, color)
		return boardCopy