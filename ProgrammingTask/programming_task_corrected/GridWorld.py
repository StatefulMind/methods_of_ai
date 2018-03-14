from UI import select_grids
from UI import select_iterations
from UI import check_interactive
from UI import select_discount
from UI import select_step_cost
from UI import select_convergence
from UI import check_running
from UI import select_evaluations
from UI import run_and_print_grid_per_step
from UI import get_next_iteration_steps
import sys
from Grid import Grid
from Evaluator import Evaluator


def main():
    running = True
    while running:
        grid = Grid(grid_file=select_grids())

        print("Our GridWorld looks as follows:")
        grid.print_grid()
        old_policy = grid.get_policy_grid()

        # ask how high the discount factor should be
        discount = select_discount()
        # ask about the cost each step
        step_cost = select_step_cost()

        # ask if user wants each iteration in single steps
        interactive = check_interactive()

        if not interactive == 'interactive':
            # ask about number of evaluation steps
            evaluation_steps = select_evaluations()

            # ask how many iterations should be done
            iterations = select_iterations()

            # ask about convergence epsilon value
            convergence = select_convergence()

        else:
            # in interactive mode, do as many steps as the user wants without convergence
            evaluation_steps = 2**200
            convergence = 0
            iterations = 0

        print('The initial randomly generated policy:')
        grid.print_policy()
        print()
        # init the Evaluator with the selected value for the learning steps
        evaluator = Evaluator(grid=grid)
        converged = False

        for step in range(evaluation_steps):
            if interactive == 'interactive':
                iterations = get_next_iteration_steps()
                if iterations <= 0:
                    print_and_quit(evaluator)
            evaluator.iterate(iterations=iterations, step_cost=step_cost,
                              discount=discount,
                              convergence_epsilon=convergence)
            evaluator.evaluate()
            run_and_print_grid_per_step(grid, step)
            if interactive == 'interactive':
                print("The corresponding evaluation values are")
                evaluator.print_grid_eval_values()
                print()
            new_policy = evaluator._grid.get_policy_grid()
            # A static state is reached when the old and the evaluated policies are the same
            if old_policy == new_policy:
                print("Policy converged!")
                print_and_quit(evaluator, _quit=False)
                if not interactive == 'interactive':
                    converged = True
                    break
                else:
                    print("If this does not seem to be the final policy, you might want to try more iteration steps\n")
            old_policy = new_policy

        if not converged:
            print("The policy did not converge with the parameters you chose."
                  "You might want to run again with different parameters.")

        # interact if program should run again
        running = check_running()


def print_and_quit(evaluator, _quit=True):
    """
    Prints the best found policy with the corresponding evaluation and terminates the program.
    """
    if _quit:
        print("Ending the program")
    print("The policy is now:")
    evaluator._grid.print_policy()
    print("\nThe evaluation values of this policy are:")
    evaluator.print_grid_eval_values()
    if _quit:
        print("Thank you for running our program")
        sys.exit(0)


if __name__ == '__main__':
    main()
