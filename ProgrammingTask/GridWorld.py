import argparse
from Grid import Grid
from Evaluator import Evaluator


# instantiate parser
parser = argparse.ArgumentParser(prog='Grid World Evaluator',
                                 description='''Read grid-file from stdin,
parse and print grid file accordingly.''',
                                 usage='%(prog)s [options]',
                                 prefix_chars='-')
parser.add_argument('grid_file', help='path to input .grid file')
parser.add_argument('-i', '--iter', default=50, type=int,
                   help='number of iterations performed by the policy iteration')
parser.add_argument('-e', '--eval', default=50, type=int,
                   help='number of evaluations on the iterated policy')
parser.add_argument('-s', '--step', action='store_true',
                    help='manual iteration for policy iteration')
parser.add_argument('-c', '--cost', default = 0.04,
                    help='cost for every step' )
parser.add_argument('-g', '--gamma', default=1, type=float,
                    help='discount value gamma')
parser.add_argument('-eps', '--epsilon', default=0, type=float,
                    help='discount value gamma')
parser.add_argument('-v', '--verbose', action='store_true',
                    help='print verbose output (every intermediate evaluation step)')
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
    grid = Grid(grid_file=args.grid_file)

    print("Our GridWorld looks as follows:")
    grid.print_grid()

    if not args.step:
        run_automatic_mode(grid)
    else:
        run_interactive_mode(grid)

if __name__ == '__main__':
    main()