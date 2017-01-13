import exceptions

class BoardController:
    '''
    The controller of the board, determines the rules of the game
    '''
    def __init__(self, white_id=1, black_id=2, blank_id=0, black_offensive=True):
        self.white_id = white_id
        self.black_id = black_id
        self.blank_id = blank_id
        if black_offensive:
            self.offensive_id = black_id
            self.defensive_id = white_id
        else:
            self.offensive_id = white_id
            self.defensive_id = black_id

    def bind_view(self, view):
        self.view = view

    def bind_board(self, board):
        self.board = board
        self.board_size = board.size

    def check_winner(self):
        cur_player_color = self.get_cur_play_color()
        last_player_color = self.black_id if cur_player_color == self.white_id else self.white_id
        last_player_trace = self._get_correspond_color_trace(last_player_color)
        winner = 0
        if len(last_player_trace) > 0:
            last_step_location = last_player_trace[-1]
            winner = last_player_color if self.check_win(last_step_location, last_player_color) else winner
        return winner


    def check_win(self, location, color):
        '''
        Given the location and the corresponding color of particular round, the controller decide wheather the player wins the game
        location: (int, int), the x, y coordinate of the location
        color: white_id or black_id
        '''
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
        return len(self.board.white_trace) + len(self.board.black_trace) == 0

    def location_available(self, location):
        availabel = True
        try:
            availabel = self.board.location_available(location)
        except Exception as e:
            availabel = False
        return availabel

    def get_cur_play_color(self):
        offensive_trace = self._get_correspond_color_trace(self.offensive_id)
        defensive_trace = self._get_correspond_color_trace(self.defensive_id)
        if len(offensive_trace) > len(defensive_trace):
            return self.defensive_id
        else:
            return self.offensive_id

    def get_last_play_color(self):
        cur_player_color = self.get_cur_play_color()
        last_player_color = self.black_id if cur_player_color == self.white_id else self.white_id
        return last_player_color

    def regret(self, color):
        regret_trace = self._get_correspond_color_trace(color)
        opponent_trace = self.board.black_trace if regret_trace == self.board.white_trace else self.board.white_trace
        if len(regret_trace) == 0:
            print('There are no enough rounds to regret.')
        else:
            regret_location = regret_trace[-1]
            self.board.update(regret_location, 0)
            if len(opponent_trace) > 0:
                opponent_location = opponent_trace[-1]
                self.board.update(opponent_location, 0)

    def display(self):
        self.view.display_board(self.board)

    def _get_correspond_color_trace(self, color):
        if color == self.white_id:
            return self.board.white_trace
        elif color == self.black_id:
            return self.board.black_trace
        else:
            return None