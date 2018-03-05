import argparse
from Grid import Grid
from Learner import Learner
from UI import select_grids
from UI import select_start
from UI import check_running
from UI import select_epsilon
from UI import select_episodes
from UI import select_convergence
from UI import check_version
from UI import check_interactive
from UI import select_delay_time
from UI import select_learning_rate

parser = argparse.ArgumentParser(prog='QLearn',
                                 description='''Read grid-file,
                                 parse and print grid file and apply Q-learning.''',
                                 usage='%(prog)s [options]',
                                 prefix_chars='-')
parser.add_argument('-g', '--grid_file', help='path to input .grid file')
args = parser.parse_args()


def main():
    running = True
    #check_version()
    while running:
        grid = Grid(select_grids())
        print('Your .grid file:')
        grid.print_grid()
        starting_point = select_start()
        epsilon = select_epsilon(0.4)
        episodes = select_episodes()
        interactive = check_interactive()
        delay_time=select_delay_time()
        convergence = select_convergence()
        learning_rate = select_learning_rate()

        print('Initial randomly generated policy"')
        grid.print_policy()
        print("")
        learner = Learner(grid=grid, position=starting_point,
                          epsilon_soft=epsilon, learning_rate=learning_rate)
        learner.learn(episodes=episodes,
                      convergence=convergence, interactive=interactive, delay_time=delay_time)
        running = check_running()


if __name__ == "__main__":
    main()
