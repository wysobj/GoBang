import board

board = board.Board()
board.update((2,7), 2)
board.update((3,6), 2)
board.update((4,5), 2)
board.update((5,4), 2)
board.update((6,3), 2)
print(board.winner())
print(board.model)