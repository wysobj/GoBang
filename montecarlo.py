import datetime, math, random

class MonteCarloAI:
    '''
    A gobang AI implemented by MCTS algorithm.
    '''
    def __init__(self, controller, color, move, verbose=True):
        self.controller = controller
        self.color = color
        self.move = move
        self.time_interval = datetime.timedelta(seconds = 30)
        self.verbose = verbose
        self.critical_area = 1

    def get_location(self):
        self.plays = {}
        self.wins = {}
        board = self.controller.board
        begin = datetime.datetime.utcnow()
        board_size = self.controller.board_size
        game = 0
        if self.controller.is_board_empty():
            return (int(board_size / 2), int(board_size / 2))
        while datetime.datetime.utcnow() - begin < self.time_interval:
            self.simulation(board)
            game = game + 1
        if self.verbose:
            print("AI runs "+str(game)+" simulations.")
        self.controller.bind_board(board)
        best_step = None
        best_prob = - float('inf')
        next_steps = self._get_next_steps(board)
        for step in next_steps:
            next_board = self._get_next_board(board, step)
            play_num = self.plays.get(next_board, 1)
            win_num = self.wins.get(next_board, 0)
            if self.verbose:
                print("PlayNums:"+str(play_num)+", WinNums:"+str(win_num))
            prob = win_num / play_num
            if prob >= best_prob:
                best_step = step
                best_prob = prob
        return best_step

    def simulation(self, board):
        gamma= 0.2
        visited = set()
        extended = False
        winner = 0
        cur_board = board
        for i in range(self.move):
            next_steps = self._get_next_steps(cur_board)
            self.controller.bind_board(cur_board)
            cur_color = self.controller.get_cur_play_color()
            next_boards = [self._get_next_board(cur_board, step) for step in next_steps]
            next_choiced_board = None
            if all(self.plays.get(next_board) for next_board in next_boards):
                log_sum = math.log(sum(self.plays.get(next_board) for next_board in next_boards))
                best_next_board = None
                best_ucb = -float('inf')
                for next_board in next_boards:
                    play_num = self.plays.get(next_board, 1)
                    win_num = self.wins.get(next_board, 0)
                    ucb = win_num / play_num + gamma * math.sqrt(2 * log_sum / play_num)
                    if ucb >= best_ucb:
                        best_next_board = next_board
                        best_ucb = ucb
                next_choiced_board = best_next_board
            else:
                choice = random.randint(0, len(next_boards) - 1)
                next_choiced_board = next_boards[choice]

            cur_board = next_choiced_board

            if not extended and next_choiced_board not in self.plays:
                self.plays[next_choiced_board] = 0
                self.wins[next_choiced_board] = 0
                extended = True

            visited.add(next_choiced_board)
            self.controller.bind_board(next_choiced_board)
            winner = self.controller.check_winner()
            if winner != 0:
                break
            
            draw = self.controller.check_draw()
            if draw:
                break

        for visited_board in visited:
            if visited_board not in self.plays.keys():
                continue
            self.plays[visited_board] += 1
            self.controller.bind_board(visited_board)
            visited_board_color = self.controller.get_last_play_color()
            if winner == visited_board_color:
                self.wins[visited_board] += 1
            elif winner != visited_board_color and winner != 0:
                self.wins[visited_board] -= 1

    def _get_next_steps(self, curBoard):
        steps = set()
        for i in range(self.controller.board_size):
            for j in range(self.controller.board_size):
                location = (i, j)
                location_valid = self.controller.location_available(location)
                if not location_valid:
                    continue
                critical = self._check_critical(location)
                if critical:
                    steps.add(location)
        return steps

    def _check_critical(self, location):
        start_row = location[0] - self.critical_area
        start_col = location[1] - self.critical_area
        end_row = location[0] + self.critical_area
        end_col = location[1] + self.critical_area
        for i in range(start_row, end_row+1):
            for j in range(start_col, end_col+1):
                location = (i, j)
                try:
                    location_color = self.controller.board.color_of_location(location)
                except Exception as e:
                    continue
                if location_color != self.controller.blank_id:
                    return True
        return False

    def _get_next_board(self, board, location):
        board_copy = board.fork()
        self.controller.bind_board(board)
        color = self.controller.get_cur_play_color()
        board_copy.update(location, color)
        return board_copy