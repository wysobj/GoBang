from exceptions import UnSupportException

class BaseView:

    def __init__(self, board):
        self.board = board
        self.size = board.size

    def display_board(self, board):
        raise UnSupportException()