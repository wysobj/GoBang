import exceptions

class Board:

    #white = 1, black = 2
    def __init__(self, **args):
        size = args.get('size', 10)
        if size > 20:
            print("Board size too large, set to maximum size :20")
            size = 20
        if size < 10:
            print("Board size too small, set to minimun size: 10")
            size = 10
        self.size = size
        self.blank_color = args.get('blank', 0)
        self.white_color = args.get('white', 1)
        self.black_color = args.get('black', 2)
        self.white_trace = []
        self.black_trace = []

    def update(self, location, new_color):
        self.boundry_check(location)
        if location in self.white_trace:
            old_color = self.white_color
            conflict_trace = self.white_trace
        elif location in self.black_trace:
            old_color = self.black_color
            conflict_trace = self.black_trace
        else:
            conflict_trace = None
            old_color = self.blank_color
        if old_color != self.blank_color and new_color != self.blank_color:
            raise exceptions.OccupiedException()
        elif old_color != self.blank_color and new_color == self.blank_color:
            conflict_trace.remove(location)
        elif old_color == self.blank_color and new_color != self.blank_color:
            set_trace = self.white_trace if new_color == self.white_color else self.black_trace
            set_trace.append(location)
        else:
            raise exceptions.InvalidePlayLocationException()

    def color_of_location(self, location):
        self.boundry_check(location)
        if location in self.white_trace:
            return self.white_color
        elif location in self.black_trace:
            return self.black_color
        else:
            return self.blank_color

    def boundry_check(self, location):
        row = location[0]
        col = location[1]
        if row >= self.size or col >= self.size or row < 0 or col < 0:
            raise exceptions.OutOfRangeException()

    def location_available(self, location):
        self.boundry_check(location)
        return location not in self.white_trace and location not in self.black_trace

    def rounds_played(self):
        return len(self.white_trace) + len(self.black_trace)

    def fork(self):
        new_board = Board(size = self.size)
        new_board.size = self.size
        new_board.blank_color = self.blank_color
        new_board.white_color = self.white_color
        new_board.black_color = self.black_color
        new_board.white_trace = [wl for wl in self.white_trace]
        new_board.black_trace = [bl for bl in self.black_trace]
        return new_board

    def __hash__(self):
        hashcode = 0
        for wc in self.white_trace:
            hashcode += wc[0] * self.size * self.size + wc[1]
        for bc in self.black_trace:
            hashcode += bc[0] * self.size * self.size + bc[1]
        hashcode += self.rounds_played() * self.size * self.size
        return hashcode

    def __eq__(self, other):
        if self.rounds_played() != other.rounds_played():
            return False
        for i in range(len(self.white_trace)):
            if self.white_trace[i] != other.white_trace[i]:
                return False
        for i in range(len(self.black_trace)):
            if self.black_trace[i] != other.black_trace[i]:
                return False
        return True

