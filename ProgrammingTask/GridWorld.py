from UI import select_grids
from UI import select_iterations
from UI import check_interactive
from UI import select_discount
from UI import select_step_cost
from UI import select_convergence
from UI import select_learning_rate
from UI import check_running
from UI import select_evaluations
from UI import run_and_print_grid_per_step
from UI import get_next_evalutation_step
from UI import get_next_iteration_step
from UI import check_next_step
import sys
from Grid import Grid
from Evaluator import Evaluator


def run_interactive_mode(grid):

        iterations = input('How many iteration steps do you want to perform (int, default = {})? '.format(default_iter))
        if iterations == '':
            iterations = default_iter
        else:
            iterations = int(iterations)
        eval_steps = input('How many evaluation steps do you want to perform (int, default = {})?'.format(default_eval))
        if eval_steps == '':
            eval_steps = default_eval
        else:
            eval_steps = int(eval_steps)

        for eval_step in range(eval_steps):
            evaluator.iterate(iterations, step_cost=args.cost, discount=args.gamma)
            evaluator.evaluate()

        print("")
        print("Finished {} evaluation steps. Optimized policy:".format(eval_step+1))
        grid.print_policy()
        print("")


def main():
    running = True
    while running:
        grid = Grid(grid_file=select_grids())

        print("Our GridWorld looks as follows:")
        grid.print_grid()
        old_policy = grid.get_policy_grid()

        # ask how many iterations should be done
        iterations = select_iterations()
        # ask how hight the discount factor should be
        discount = select_discount()
        # ask about the cost each step
        step_cost = select_step_cost()
        # ask about convergence epsilon value
        convergence = select_convergence()
        # ask about the discount gamma ?
        gamma = select_learning_rate()
        # ask about number of evaluation steps
        evaluation_steps = select_evaluations()

        # ask if user wants each iteration in single steps
        interactive = check_interactive()

        print('The initial randomly generated policy:')
        grid.print_policy()
        # init the Evaluator with the selected value for the learning steps
        evaluator = Evaluator(grid=grid)
        for step in evaluation_steps:
            if interactive == 'interactive':
                check_next_step()
                iterations = 1 if get_next_iteration_step() is True else print_done_and_terminate()
                
            evaluator.iterate(iterations=iterations, step_cost=step_cost,
                          discount=discount,
                          convergence_epsilon=convergence)
            evaluator.evaluate()
            run_and_print_grid_per_step(grid, step)
        new_policy = grid.get_policy_grid()
        # check for convergence if both grids are the same
        if old_policy == new_policy:
            print("Policy converged! ")

        # interact if program should run again
        running = check_running()


if __name__ == '__main__':
    main()


def print_done_and_terminate():
    print('You have not confirmed - exiting now.'
          'Thank you!')
    sys.exit(0)
