from board import Board
from controller import BoardController
from montecarlo import MonteCarloAI
from cmder_view import CmderView
import pickle, os, datetime

'''
This file is a demo where you can simulate ai combating with each other,
the simulation results will be saved in the "save_dir" dir
'''


size = 10
ai1_color = 1
ai2_color = 2
view = CmderView(white_color=ai1_color, black_color=ai2_color)
controller = BoardController()
controller.bind_view(view)
ai1 = MonteCarloAI(controller, ai1_color, verbose=False, simulation_num=12, time_limit=180, critical_area=1)
ai2 = MonteCarloAI(controller, ai2_color, verbose=False, simulation_num=12, time_limit=180, critical_area=1)
save_freq = 100
save_file = "simulation"
save_dir = "simulation_results"
if not os.path.isdir(save_dir):
    os.mkdir(save_dir)
simulations = []
save_id = 1
simulation_idx = 0
simulation_num = 10000
while simulation_idx <= simulation_num:
    result = -1
    board = Board(size=size, white=ai1_color, black=ai2_color)
    controller.bind_board(board)
    rounds = 0
    trace = []
    while True:
        rounds += 1
        dynamic_timelimit = int(rounds/2) * 2
        tl = dynamic_timelimit if dynamic_timelimit <= 30 else 30
        ai1.time_limit = datetime.timedelta(seconds=tl)
        ai2.time_limit = datetime.timedelta(seconds=tl)
        cur_color = controller.get_cur_play_color()
        prev_color = controller.get_prev_play_color()
        draw = controller.check_draw()
        if draw:
            result = 0
            break
        winner_color = controller.check_winner()
        if winner_color == ai1_color:
            result = ai1_color
            break
        elif winner_color == ai2_color:
            result = ai2_color
            break
        if cur_color == ai1_color:
            ai1_location, ai1_confidence = ai1.get_location()
            controller.play(ai1_location, ai1_color)
            trace.append((ai1_location, ai1_confidence))
        elif cur_color == ai2_color:
            ai2_location, ai2_confidence = ai2.get_location()
            controller.play(ai2_location, ai2_color)
            trace.append((ai2_location, ai2_confidence))
    simulations.append((trace, result))
    simulation_idx += 1
    print("simulation "+str(simulation_idx)+" done")
    if simulation_idx % save_freq == 0:
        pickle_name = save_dir + os.path.sep +save_file + str(save_id) + ".pkl"
        save_id += 1
        pickle.dump(simulations, open(pickle_name, "wb"))
        print("save to "+pickle_name+"...done")
        simulations = []
