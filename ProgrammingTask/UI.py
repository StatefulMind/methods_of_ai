try:
    import os
    import numpy as np
    import sys
    from time import sleep
except ImportError as e:
    print('An Exception occurred in while importing modules !')
    print(e)

GRID_DIR = './grids'


def check_version():
    """
    Checks if dependencies are met and imported packages have the right version
    exits script if requirements are not met
    """
    py_check = False
    numpy_check = False
    python_version = sys.version_info
    if python_version[0] != 3 or python_version[1] < 6 or python_version[2] < 4:
        py_check = True
        invalid = 'python'
    numpy_version = int(('').join(np.__version__.split('.')))
    if numpy_version < 1133:
        numpy_check = True
        invalid = 'numpy'
    if py_check or numpy_check:
        print('Looks like you are not running the required {invalid} version !\n'
              '------------------------------------------------------------\n'
              'Please refer to the README and check the dependencies...\n'.format(invalid=invalid))
        sleep(1)
        print(".")
        sleep(1)
        print(".")
        sleep(1)
        print('EXITING NOW.')
        sys.exit(1)


def check_running():
    """
    Checks if the user wants to continue running the program
    if user enters n/N/No/NO False will be returned that leads to termination of script
    :returns running boolean:
    """
    while True:
        user_in = input('\n\nDo you want to continue with a new run? [y/n] ')
        if user_in == 'y' or user_in == 'Y' or user_in == 'Yes' or user_in == 'YES':
            running = True
            break
        if user_in == 'n' or user_in == 'N' or user_in == 'No' or user_in == 'NO':
            running = False
            break
        else:
            continue
    return running


def check_interactive(interactive=None):
    """
    Reads from user input if the learning is run iteratively - in interactive mode
    or if learning is run automatically without user intervention.
    :param interactive: Can take default value here.
    :return 'interactive' or  'automatic':
    """
    while not interactive:
        user_in = str(input("Do you want to run in interactive mode [i] or automatic (any key)? "))
        interactive = 'interactive' if user_in == 'i' else 'automatic'
        print()
    return interactive


def check_next_episode(user_continue=None):
    """
    Reads from input if the user wants to execute the next episode.
    :param user_continue: Can take default value here.
    :return boolean: False or true, depending on if the user wants to continue
    """
    if not user_continue:
        user_in = input('Next Episode? Press enter to continue, "n" to stop. ')
        if user_in == 'n':
            user_continue = False
        else:
            user_continue = True
    return user_continue


def check_next_step(user_continue=None):
    """
    Reads from input if the user wants to execute the next episode.
    :param user_continue: Can take default value here.
    :return boolean: False or true, depending on if the user wants to continue
    """
    if not user_continue:
        user_in = input('Do the next step ? Press enter to continue, "n" to stop. ')
        user_continue = False if user_in == 'n' else True
    return user_continue


def select_grids(grid_file=GRID_DIR):
    """
    displays provided directory and user chooses from files in directory
    or parsing the .grid file accordingly
    :returns grid: A grid file
    """
    if os.path.isdir(grid_file):
        print('Grid Files in {g_dir} is:'.format(g_dir=grid_file))
        all_files = os.listdir(grid_file)
        for i, _file in enumerate(all_files):
            print('[{number}]   -   {name}'.format(number=i, name=_file))
        index = None
        while not index:
            try:
                index = int(input('Select .grid file by number... '))
                print()
                # if integer can be casted without error and should be in limits
                if not 0 <= index < len(all_files):
                    raise ValueError
            except ValueError as e:
                print('Not an integer in the correct range...')
                print(e)
                index = None
        grid_file = os.path.join(GRID_DIR, all_files[index])
    if grid_file[-4:] == 'grid':
        grid_path = grid_file
    else:
        print('Oops. You have provided the wrong file!')
        raise FileNotFoundError
    return grid_path


def select_start(run_mode=None):
    """
    Reads and assigns the mode for selecting the start value
    either static - always at lower left corner (0,2) or random for each episode
    :param run_mode:
    :return 'static' or 'random':
    """
    while not run_mode:
        run_mode = int(input("Select [0] for 'static' start at the lower left corner or "
                             "[1] for 'random' starting points... "))
        if run_mode == 0 or run_mode == 1:
            run_mode = 'static' if run_mode == 0 else 'random'
            break
        else:
            print('Selection not in range')
            run_mode = None
            continue
    return run_mode


def select_epsilon(epsilon=None):
    """
    Reads epsilon value for the epsilon-soft policy,
    encodes greek lower epsilon as unicode.
    :param epsilon: Can take default value.
    :return float epsilon:
    """
    while not epsilon:
        epsilon = float(input("Select a value for the {epsilon} between 0..1 \n"
                              "where 0 --> greedy run and 1 --> random run... ".format(epsilon='\u03B5')))
        if 0 <= epsilon <= 1:
            break
        else:
            print('Value is not in range!')
            epsilon = None
            continue
    return epsilon


def select_episodes(episodes=None):
    return int(check_input_and_return("number of episodes", episodes))


def select_iterations(iterations=None):
    return int(check_input_and_return("number of iterations to be done before every evaluation", iterations))


def select_convergence(convergence=None):
    """
    Read convergence value from input
    for later usage in the learn function.
    :param convergence: Can take default value.
    :return convergence value:
    """
    while not convergence:
        convergence = float(input("Enter a convergence value... \n"
                                  "-----------------------------\n"
                                  "HELP: \n"
                                  "The absolute difference of the evaluation values from "
                                  "current vs. next assignment \n"
                                  "leading to termination if "
                                  "this value is satisfied\n"
                                  "======== \n"
                                  "... "))
        if 0 <= convergence <= 20:
            break
        else:
            print('Your convergence value is either too high or too low.')
            convergence = None
            continue
    return convergence


def select_delay_time(delay_time=None):
    return float(check_input_and_return("time (in s) to sleep between steps",
                                        delay_time))


def select_learning_rate(learning_rate=None):
    return float(check_input_and_return("learning rate", learning_rate))


def select_discount(discount=None):
    return float(check_input_and_return("discount factor", discount))


def select_step_cost(step_cost=None):
    return float(check_input_and_return("step cost", step_cost, can_be_negative=True))


def select_evaluations(evaluations=None):
    return int(check_input_and_return("evaluations", evaluations))


def check_input_and_return(value_name, check_value, can_be_negative=False):
    while not check_value:
        check_value = input(("Enter {}... ".format(value_name)))
        if can_be_negative or float(check_value) >= 0.0:
            print()
            break
        else:
            print("This value cannot be negative!")
            continue
    return check_value


def run_and_print_grid_per_step(grid, step_count):
    print("Evaluation step {}...".format(step_count+1))
    grid.print_policy()
    print("\n")


def get_next_iteration_step():
    iteration = input("Do you want to iterate? [y/n] ")
    iteration = True if iteration == 'y' else False
    return iteration


def get_next_iteration_steps():
    iteration = input("How many steps do you want to iterate and evaluate afterwards? Type [n] or [0] to stop")
    print()
    iteration = 0 if iteration == "n" else int(iteration)

    return iteration


def get_next_evaluation_step():
    evaluation = bool(input("Do you want to evaluate and improve the policy? [y/n] "))
    evaluation = True if evaluation == 'y' else False
    return evaluation
