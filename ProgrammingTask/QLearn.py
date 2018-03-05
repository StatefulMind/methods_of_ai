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


def main():
    running = True
    # check_version()
    while running:
        grid = Grid(select_grids())
        print('Your .grid file:')
        grid.print_grid()
        #Asks the user if each episode should start in the left corner or randomly
        starting_point = select_start()
        #Asks the user to enter epsilon for the eps-soft-policy
        epsilon = select_epsilon()
        #Asks the user how many episodes should be done
        episodes = select_episodes()
        #Asks the user if he wants to confirm each single step
        interactive = check_interactive()
        #Asks the user if the program should sleep after each step
        delay_time=select_delay_time()
        #Asks the user to select a value when the program should consider two q_tables as the same
        convergence = select_convergence()
        #Asks the user to select a learning rate
        learning_rate = select_learning_rate()

        print('Initial randomly generated policy"')
        grid.print_policy()
        print("")
        #Init of the learner
        learner = Learner(grid=grid, position_flag=starting_point,
                          epsilon_soft=epsilon, learning_rate=learning_rate)
        #Start the learning process
        learner.learn(episodes=episodes,
                      convergence=convergence, interactive=interactive, delay_time=delay_time)
        #Checks if the user wants the whole thing to run again
        running = check_running()


if __name__ == "__main__":
    main()
