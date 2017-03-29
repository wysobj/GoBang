from cmder_view import CmderView
from board import Board
from controller import BoardController
from montecarlo import MonteCarloAI
import random
import exceptions

class App:

    def __init__(self):
        controller = BoardController()
        size_get = False
        blank_color = 0
        white_color = 1
        black_color = 2
        while not size_get:
            size = input("Please enter the board size( 10-20 ): ")
            size_get = True
            try:
                size = int(size)
            except ValueError as e:
                print("Invalid input type, please enter a digital number.")
                size_get = False
        
        if size > 20:
            print("Board size too large, set to maximum size :20")
            size = 20
        if size < 10:
            print("Board size too small, set to minimun size: 10")
            size = 10

        player_color = 0
        while player_color == 0:
            color = input("Please enter the piece color( black or white, black is the offensive color ): ")
            color = color.strip()
            if color == "white":
                player_color = white_color
                self.player_color_text = color
            elif color == 'black':
                player_color = black_color
                self.player_color_text = color
            else:
                print("Invalid color, please reenter the color 'black' or 'white'.")

        self.player_color = player_color
        self.ai_color = black_color if player_color == white_color else white_color
        view = CmderView(white_color=white_color, black_color=black_color)
        controller.bind_view(view)
        model = Board(size=size, white_color=white_color, black_color=black_color, blank_color=blank_color)
        controller.bind_board(model)
        self.controller = controller
        self.ai = MonteCarloAI(controller, self.ai_color, simulation_num=15, time_limit=20)

    def start(self):
        winner = 0
        while winner == 0:
            self.controller.display()
            cur_play_color = self.controller.get_cur_play_color()
            if cur_play_color == self.ai_color:
                print("")
                print("AI is thinking...")
                ai_location, confidence = self.ai.get_location()
                self.controller.play(ai_location, self.ai_color)
            else :
                command_parsed = False
                while not command_parsed:
                    command = input("Your next operation"+"( Your color is "+self.player_color_text+" )"+": ")
                    command = command.strip()
                    if command == "help":
                        self.print_help()
                    elif command == "exit":
                        print("exit!")
                        exit(0)
                    elif command == "restart":
                        self.restart()
                        command_parsed = True
                    elif command == "regret":
                        regret = self.controller.regret()
                        if regret == False:
                            print("There are no enough rounds to regret.")
                        command_parsed = True
                    elif len(command.split(" ")) == 2:
                        location = command.split(" ")
                        row = location[0]
                        col = location[1]
                        try:
                            row = int(row)
                            col = int(col)
                        except ValueError as e:
                            print("Invalid location format.")
                        location_valid = True
                        player_location = (row - 1, col - 1)
                        try:
                            self.controller.play(player_location, self.player_color)
                        except exceptions.OccupiedException as e:
                            print("The location you specify is already occupied.")
                            location_valid = False
                        except exceptions.OutOfRangeException as e:
                            print("The location you specify is out of the board range.")
                            location_valid = False
                        if location_valid:
                            command_parsed = True
                    else:
                        print("Invalid command.")
            draw = self.controller.check_draw()
            if draw:
                self.controller.display()
                print("Draw!")
                exit(0)
            winner = self.controller.check_winner()
            if winner == self.player_color:
                self.controller.display()
                print("You win!")
                exit(0)
            elif winner == self.ai_color:
                self.controller.display()
                print("You lose!")
                exit(0)


    def print_help(self):
        print("command: \"regret\",  usage: roll back to the previous board state.")
        print("command: \"rowID colID\", usage: location at the rowID th row and colID th column.")
        print("command: \"restart\", usage: start a new game.")
        print("command: \"exit\", usage: quite the game.")

    def restart(self):
        view = views.BoardView()
        controller = BoardController()
        view = CmderView()
        controller.bind_view(view)
        model = Board(size=size)
        controller.bind_board(model)
        self.ai = MonteCarloAI(controller, ai_color, 20)
        self.start()
