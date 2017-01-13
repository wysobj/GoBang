from cmder_view import CmderView
from board import Board
from controller import BoardController
from montecarlo import MonteCarloAI

view = CmderView()
model = Board(size=10)
controller = BoardController()
ai_color = 2
player_color = 1
ai = MonteCarloAI(controller, ai_color, 20)
controller.bind_board(model)
controller.bind_view(view)
for i in range(10):
    ai_location = ai.get_location()
    controller.play(ai_location, ai_color)
    player_location = (i, 0)
    valid = controller.location_available(player_location)
    while not valid:
        player_location = (player_location[0]+1, 0)
        valid = controller.location_available(player_location)
    controller.play(player_location, player_color)
    controller.display()
    print(model.white_trace)
    print(model.black_trace)
    print(controller.get_cur_play_color())
    print(controller.check_winner())

