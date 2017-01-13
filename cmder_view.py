from base_view import BaseView

class CmderView(BaseView):

    '''
    View that support print the board in the Cmder console 
    '''
    def __init__(self):
        pass

    def display_board(self, board):
        self.size = board.size
        self._print_aboveLabel()
        for i in range(self.size):
            self._print_horizental_boundry()
            row_view = ''
            if i < 9:
                row_view = row_view + ' '
            row_view = row_view + str(i + 1) + '|'
            for j in range(self.size):
                piece = ''
                location = (i, j)
                if location in board.white_trace:
                    piece = ' ○'
                elif location in board.black_trace:
                    piece = ' ●'
                else:
                    piece = '  '
                piece = piece + ' |'
                row_view = row_view + piece
            print(row_view)
        self._print_horizental_boundry()

    def _print_aboveLabel(self):
        label = ' ' * 3
        for i in range(self.size):
            label = label + ' ' + str(i+1) + ' '
            if i < 9:
                label = label + ' '
        print(label)

    def _print_horizental_boundry(self):
        line = ' ' * 3
        for i in range(self.size):
            line = line + ' 一 '
        print(line)
    
    