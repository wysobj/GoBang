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
        black_offensive = args.get('black_offensive', True)
        self.trace = []
        self.offensive_color = self.black_color if black_offensive else white_color
        self.defensive_color = self.white_color if black_offensive else black_color
        self.model = [[0 for col in range(self.size)] for row in range(self.size)]

    def update(self, location, new_color):
        self.boundry_check(location)
        row = location[0]
        col = location[1]
        location_occupied = self.model[row][col] != self.blank_color
        if location_occupied and new_color != self.blank_color:
            raise exceptions.OccupiedException()
        elif location_occupied and new_color == self.blank_color:
            self.trace.remove(location)
            self.model[row][col] = new_color
        elif not location_occupied and new_color != self.blank_color:
            self.trace.append(location)
            self.model[row][col] = new_color
        else:
            raise exceptions.InvalidePlayLocationException()

    def color_of_location(self, location):
        self.boundry_check(location)
        row = location[0]
        col = location[1]
        color_of_location = self.model[row][col]
        return color_of_location

    def boundry_check(self, location):
        row = location[0]
        col = location[1]
        if row >= self.size or col >= self.size or row < 0 or col < 0:
            raise exceptions.OutOfRangeException()

    def location_available(self, location):
        self.boundry_check(location)
        return location not in self.trace

    def rounds_played(self):
        return len(self.trace)

    def fork(self):
        new_board = Board(size = self.size)
        new_board.blank_color = self.blank_color
        new_board.white_color = self.white_color
        new_board.black_color = self.black_color
        for round_idx in range(self.rounds_played()):
            round_color = self.offensive_color if round_idx%2==0 else self.defensive_color
            new_board.update(self.trace[round_idx], round_color)
        return new_board

    def __hash__(self):
        hashcode = 0
        for round_idx in range(self.rounds_played()):
            hashcode += self.trace[round_idx][0] * self.size * self.size + self.trace[round_idx][1]
        return hashcode

    def __eq__(self, other):
    #     import datetime
    #     s = datetime.datetime.utcnow()
        if other == None:
            return False
        if not isinstance(other, Board) and self.rounds_played() != other.rounds_played():
            return False
        for i in range(self.size):
            for j in range(self.size):
                if self.model[i][j] != other.model[i][j]:
                    return False
        # e = datetime.datetime.utcnow()
        # print("Compare time:"+str(e-s))
        return True
