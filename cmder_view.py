from base_view import BaseView

class CmderView(BaseView):

    '''
    View that support print the board in the Cmder console
    '''
    def __init__(self, white_color=1, black_color=2):
        self.white_color = white_color
        self.black_color = black_color
        self.white_icon = "○"
        self.black_icon = "●"
        self.prev_step_white = "◎"
        self.prev_step_black = "◉"
        pass

    def display_board(self, model, prev_location, prev_color):
        self.size = len(model)
        self._print_aboveLabel()
        prev_icon = None
        if prev_color != None:
            prev_icon = self.prev_step_white if prev_color == self.white_color else self.prev_step_black
        for i in range(self.size):
            self._print_horizental_boundry()
            row_view = ""
            if i < 9:
                row_view = row_view + " "
            row_view = row_view + str(i + 1) + "|"
            for j in range(self.size):
                piece = ""
                print_location = (i, j)
                if print_location != prev_location and model[i][j] == self.white_color:
                    piece = " " + "○"
                elif print_location != prev_location and model[i][j] == self.black_color:
                    piece = " " + "●"
                elif print_location == prev_location:
                    piece = " " + prev_icon
                else:
                    piece = " " * 2
                piece = piece + " " + "|"
                row_view = row_view + piece
            print(row_view)
        self._print_horizental_boundry()

    def _print_aboveLabel(self):
        label = ' ' * 3
        for i in range(self.size):
            label = label + " " + str(i+1) + " "
            if i < 9:
                label = label + " "
        print(label)

    def _print_horizental_boundry(self):
        line = " " * 3
        for i in range(self.size):
            line = line + " " +  "一" + " "
        print(line)
