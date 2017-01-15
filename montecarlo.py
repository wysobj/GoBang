import datetime, math, random

class MonteCarloAI:
    '''
    A gobang AI implemented by MCTS algorithm.
    '''
    def __init__(self, controller, color, simulation_num=20, time_limit=20, verbose=True, critical_area=1):
        self.controller = controller
        self.color = color
        self.simulation_num = simulation_num
        self.time_limit = datetime.timedelta(seconds = time_limit)
        self.verbose = verbose
        self.critical_area = critical_area
        self.back_trace_step = 3

    def get_location(self):
        '''
        Caculate a appropriate location for AI.
        '''
        self.plays = {}
        self.wins = {}
        board = self.controller.board
        begin = datetime.datetime.utcnow()
        board_size = self.controller.board_size()
        game = 0
        if self.controller.is_board_empty():
            lower_bound = int(board_size/3)
            upper_bound = int(2*board_size/3)
            return (random.randint(lower_bound, upper_bound), random.randint(lower_bound, upper_bound)), 0
        while datetime.datetime.utcnow() - begin < self.time_limit:
            self.simulation(board)
            game = game + 1
        if self.verbose:
            print("AI runs "+str(game)+" simulations.")
        self.controller.bind_board(board)
        best_step = None
        best_prob = - float("inf")
        next_steps = self._get_next_steps2()
        for step in next_steps:
            next_board = self._get_next_board(board, step, self.color)
            play_num = self.plays.get(next_board, 1)
            win_num = self.wins.get(next_board, 0)
            if self.verbose:
                print("PlayNums:"+str(play_num)+", WinNums:"+str(win_num))
            prob = win_num / play_num
            if prob >= best_prob:
                best_step = step
                best_prob = prob
        return best_step, best_prob

    def simulation(self, board):
        gamma= 0.1
        visited = set()
        extended = False
        winner = 0
        cur_board = board
        for i in range(self.simulation_num):
            # Be carful whenever we want to get infomation of a new board, we need to bind it to the controller first.
            self.controller.bind_board(cur_board)
            cur_play_color = self.controller.get_cur_play_color()
            next_steps = self._get_next_steps2()
            next_boards = [self._get_next_board(cur_board, step, cur_play_color) for step in next_steps]

            next_choiced_board = None
            if all(self.plays.get(next_board) for next_board in next_boards):
                nb = [self.plays.get(next_board) for next_board in next_boards]
                play_sum = sum(nb)
                log_sum = math.log(play_sum)
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
            if winner == self.controller.white_color() or winner == self.controller.black_color():
                break

            draw = self.controller.check_draw()
            if draw:
                break
        for visited_board in visited:
            if visited_board not in self.plays.keys():
                continue
            self.plays[visited_board] += 1
            self.controller.bind_board(visited_board)
            visited_board_color = self.controller.get_prev_play_color()
            has_winner = winner == self.controller.white_color() or winner == self.controller.black_color()
            if winner == visited_board_color:
                self.wins[visited_board] += 1
            elif winner != visited_board_color and has_winner:
                self.wins[visited_board] -= 1

    def _get_next_steps1(self):
        '''
        Local strategy, return the candidate locations for a particular board.
        The local strategy focus on the most recently steps of both sides,
        so this strategy is easy to get trapped and unable to jump out
        '''
        steps = set()
        valid_num = 0
        trace = self.controller.get_game_traces()
        rounds_num = len(trace)
        back_trace_num = rounds_num if self.back_trace_step > rounds_num else self.back_trace_step
        for t in range(back_trace_num):
            trace_step = trace[-(t+1)]
            neighbours = self._get_critical_area(trace_step)
            for n in neighbours:
                steps.add(n)
        if len(steps) == 0:
            old_bt = self.back_trace_step
            self.back_trace_step += 1
            steps = self._get_next_steps()
            self.back_trace_step = old_bt
        return steps

    def _get_critical_area(self, location):
        steps = set()
        row = location[0]
        col = location[1]
        for distance in range(1, self.critical_area+1):
            left = (row, col-distance)
            if self.controller.location_available(left):
                steps.add(left)
            right = (row, col+distance)
            if self.controller.location_available(right):
                steps.add(right)
            up = (row-distance, col)
            if self.controller.location_available(up):
                steps.add(up)
            down = (row+distance, col)
            if self.controller.location_available(down):
                steps.add(down)
            left_up = (row-distance, col-distance)
            if self.controller.location_available(left_up):
                steps.add(left_up)
            left_down = (row+distance, col-distance)
            if self.controller.location_available(left_down):
                steps.add(left_down)
            right_up = (row-distance, col+distance)
            if self.controller.location_available(right_up):
                steps.add(right_up)
            right_down = (row+distance, col+distance)
            if self.controller.location_available(right_down):
                steps.add(right_down)
        return steps

    def _get_next_steps2(self):
        '''
        Global strategy, return the candidate locations for a particular board.
        This strategy focus on all the neighbour locations of the steps.  
        '''
        steps = set()
        valid_num = 0
        trace = self.controller.get_game_traces()
        for t in trace:
            neighbours = self._get_blank_neighbours(t)
            for n in neighbours:
                steps.add(n)
        return steps

    def _get_blank_neighbours(self, location):
        board_size = self.controller.board_size()
        start_row = location[0] - self.critical_area
        start_row = 0 if start_row < 0 else start_row
        start_col = location[1] - self.critical_area
        start_col = 0 if start_col < 0 else start_col
        end_row = location[0] + self.critical_area
        end_row = board_size-1 if end_row >= board_size else end_row
        end_col = location[1] + self.critical_area
        end_col = board_size-1 if end_col >= board_size else end_col
        bn = []
        for i in range(start_row, end_row+1):
            for j in range(start_col, end_col+1):
                search_location = (i, j)
                if search_location == location:
                    continue
                try:
                    search_color = self.controller.color_of_location(search_location)
                except Exception as e:
                    continue
                if search_color != self.controller.white_color() and search_color != self.controller.black_color():
                    bn.append(search_location)
        return bn

    def _get_next_board(self, board, location, color):
        board_copy = board.fork()
        board_copy.update(location, color)
        return board_copy
