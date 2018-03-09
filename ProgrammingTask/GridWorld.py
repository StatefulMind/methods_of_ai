import argparse
from UI import select_grids
from UI import select_iterations
from UI import check_interactive
from UI import select_discount
from UI import select_step_cost
from UI import select_convergence
from UI import select_learning_rate
from UI import check_running
from Grid import Grid
from Evaluator import Evaluator


# instantiate parser
parser = argparse.ArgumentParser(prog='Grid World Evaluator',
                                 description='''Read grid-file from stdin,
parse and print grid file accordingly.''',
                                 usage='%(prog)s [options]',
                                 prefix_chars='-')
parser.add_argument('-e', '--eval', default=50, type=int,
                   help='number of evaluations on the iterated policy')
args = parser.parse_args()


def run_automatic_mode(grid):
    print("Running policy iteration in automatic mode")
    print("On file {}, with {} iteration steps or convergence to delta < {}, discount of {} and step cost {}".format(
        args.grid_file, args.iter, args.epsilon, args.gamma, args.cost))
    print("Will perform {} evaluations".format(args.eval))

    print("The current (randomized policy):")
    grid.print_policy()
    print("")

    evaluator = Evaluator(grid)

    old_policy = grid.get_policy_grid()
    for evaluation_step in range(args.eval):
        evaluator.iterate(args.iter, step_cost=args.cost, discount=args.gamma, convergence_epsilon=args.epsilon)
        evaluator.evaluate()

        if True:
            print("Evaluation step {} of {} done".format(evaluation_step + 1, args.eval))
            grid.print_policy()
            print("")

        new_policy = grid.get_policy_grid()
        if old_policy == new_policy:
            print("The policy converged. Terminating ahead of time")
            break
        old_policy = new_policy

    print("Policy Iteration and Evaluation finished. The optimal policy looks like this:")
    grid.print_policy()
    print("")


def run_interactive_mode(grid):
    default_iter = 50
    default_eval = 1

    evaluator = Evaluator(grid)

    print("Running in user interactive manual mode, therefore iter and eval are ignored.")
    print("Using step cost {} and discount factor {}".format(args.cost, args.gamma))
    print("The current policy is:")
    grid.print_policy()
    print("")

    old_policy = grid.get_policy_grid()
    while True:
        response = input('Continue evaluation? [y/n] ')
        if response is 'n':
            break

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

        new_policy = grid.get_policy_grid()
        if old_policy == new_policy:
            print("The policy has converged!")
        old_policy = new_policy


def main():
    running = True
    while running:
        grid = Grid(grid_file=select_grids())

        print("Our GridWorld looks as follows:")
        grid.print_grid()

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

        # ask if user wants each iteration in single steps
        interactive = check_interactive()

        print('The initial randomly generated policy:')
        grid.print_policy()
        # init the Evaluator with the selected value for the learning steps
        evaluator = Evaluator(grid=grid)
        evaluator.iterate(iterations=iterations, step_cost=step_cost,
                          discount=discount,
                          convergence_epsilon=convergence)
        running = check_running()

if __name__ == '__main__':
    main()
