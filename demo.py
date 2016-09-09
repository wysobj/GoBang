import controllers
import board
# controllers.BoardController().start()
board1 = board.Board()
board2 = board1.fork()

board2.model[1][2] = 2
boards = []
boards.append(board1)
boards.append(board2)
num, maxBoard = max((board.model[1][2], board) for board in boards)
print(maxBoard.model)
