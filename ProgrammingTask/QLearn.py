import argparse
from Grid import Grid
from Learner import Learner
from UI import select_grids
from UI import select_start
from UI import check_running
from UI import select_epsilon

parser = argparse.ArgumentParser(prog='QLearn',
                                 description='''Read grid-file,
                                 parse and print grid file and apply Q-learning.''',
                                 usage='%(prog)s [options]',
                                 prefix_chars='-')
parser.add_argument('-g', '--grid_file', help='path to input .grid file')
args = parser.parse_args()


def main():
    running = True
    while running:
        grid = Grid(select_grids())
        print('Your .grid file:')
        grid.print_grid()
        # run_mode = check_mode()
        starting_point = select_start()
        epsilon = select_epsilon()
        print('Initial generated policy')
        grid.print_policy()
        learner = Learner(grid=grid, position=starting_point, epsilon_soft=epsilon)
        learner.learn(iterations=25)
        running = check_running()


if __name__ == "__main__":
    main()