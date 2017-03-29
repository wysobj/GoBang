import exceptions

class BoardController:
    '''
    The controller of the board, determines the rules of the game.
    '''
    def __init__(self):
        self.view = None
        self.board = None

    def bind_view(self, view):
        self.view = view

    def bind_board(self, board):
        self.board = board

    def board_size(self):
        if self.board == None:
            raise exceptions.BoardUnbindException()
        else:
            return self.board.size

    def black_color(self):
        if self.board == None:
            raise exceptions.BoardUnbindException()
        return self.board.black_color

    def white_color(self):
        if self.board == None:
            raise exceptions.BoardUnbindException()
        return self.board.white_color

    def color_of_location(self, color):
        return self.board.color_of_location(color)

    def check_winner(self):
        rounds = self.board.rounds_played()
        winner = self.board.blank_color
        if rounds > 0:
            prev_play_color = self.board.defensive_color if rounds%2 == 0 else self.board.offensive_color
            prev_play_location = self.board.trace[-1]
            winner = prev_play_color if self._check_win(prev_play_location, prev_play_color) else winner
        return winner

    def _check_win(self, location, color):
        '''
        Given the location and the corresponding color of particular round, the controller decide wheather the player wins the game
        location: (int, int), the x, y coordinate of the location.
        '''
        if color != self.board.black_color and color != self.board.white_color:
            return False

        row_th = location[0]
        col_th = location[1]

        # check horizontally
        cursor = (row_th, col_th-1)
        left_right_continous = 0
        while True:
            try:
                cursor_color = self.board.color_of_location(cursor)
            except Exception as e:
                break
            if cursor_color != color:
                break
            left_right_continous += 1
            cursor = (cursor[0], cursor[1] - 1)
        cursor = (row_th, col_th+1)
        while True:
            try:
                cursor_color = self.board.color_of_location(cursor)
            except Exception as e:
                break
            if cursor_color != color:
                break
            left_right_continous += 1
            cursor = (cursor[0], cursor[1] + 1)
        left_right_continous += 1
        if left_right_continous >= 5:
            return True

        # check vertically
        cursor = (row_th-1, col_th)
        up_down_continous =0
        while True:
            try:
                cursor_color = self.board.color_of_location(cursor)
            except Exception as e:
                break
            if cursor_color != color:
                break
            up_down_continous += 1
            cursor = (cursor[0] - 1, cursor[1])
        cursor = (row_th+1, col_th)
        while True:
            try:
                cursor_color = self.board.color_of_location(cursor)
            except Exception as e:
                break
            if cursor_color != color:
                break
            up_down_continous += 1
            cursor = (cursor[0]+1, cursor[1])
        up_down_continous += 1
        if up_down_continous  >= 5:
            return True

        # check left_down diagonal
        cursor = (row_th-1, col_th-1)
        left_down_continous =0
        while True:
            try:
                cursor_color = self.board.color_of_location(cursor)
            except Exception as e:
                break
            if cursor_color != color:
                break
            left_down_continous += 1
            cursor = (cursor[0]-1, cursor[1]-1)
        cursor = (row_th+1, col_th+1)
        while True:
            try:
                cursor_color = self.board.color_of_location(cursor)
            except Exception as e:
                break
            if cursor_color != color:
                break
            left_down_continous += 1
            cursor = (cursor[0]+1, cursor[1]+1)
        left_down_continous += 1
        if left_down_continous  >= 5:
            return True

        # check right_down diagonal
        cursor = (row_th-1, col_th+1)
        right_down_continous =0
        while True:
            try:
                cursor_color = self.board.color_of_location(cursor)
            except Exception as e:
                break
            if cursor_color != color:
                break
            right_down_continous += 1
            cursor = (cursor[0]-1, cursor[1]+1)
        cursor = (row_th+1, col_th-1)
        while True:
            try:
                cursor_color = self.board.color_of_location(cursor)
            except Exception as e:
                break
            if cursor_color != color:
                break
            right_down_continous += 1
            cursor = (cursor[0]+1, cursor[1]-1)
        right_down_continous += 1
        if right_down_continous  >= 5:
            return True

        return False

    def check_draw(self):
        return self.board.rounds_played() == self.board.size * self.board.size

    def play(self, location, color):
        self.board.update(location, color)

    def is_board_empty(self):
        return self.board.rounds_played() == 0

    def location_available(self, location):
        availabel = True
        try:
            availabel = self.board.location_available(location)
        except Exception as e:
            availabel = False
        return availabel

    def get_cur_play_color(self):
        '''
        return the color of the player taking the next step.
        '''
        cur_play_color = self.board.defensive_color if self.board.rounds_played()%2 == 1 else self.board.offensive_color
        return cur_play_color

    def get_prev_play_color(self):
        '''
        return the color of the most recently step.
        '''
        prev_play_color = self.board.defensive_color if self.board.rounds_played()%2 == 0 else self.board.offensive_color
        return prev_play_color

    def get_game_traces(self):
        return self.board.trace

    def regret(self, color):
        if len(self.board.trace) < 2:
            return False
        else:
            prev_round_location = regret_trace[-1]
            self.board.update(prev_round_location, self.board.blank_color)
            pprev_round_location = regret_trace[-2]
            self.board.update(pprev_round_location, self.board.blank_color)
            return True

    def display(self):
        if self.view == None:
            raise exceptions.ViewUnbindException()
        if self.board == None:
            raise exceptions.BoardUnbindException()
        prev_loc = None
        prev_color = None
        if len(self.board.trace) > 0:
            prev_color = self.get_prev_play_color()
            prev_loc = self.board.trace[-1]
        self.view.display_board(self.board.model, prev_location=prev_loc, prev_color=prev_color)
