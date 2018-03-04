try:
    import os
    import numpy as np
    import itertools
    import argparse
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
        user_in = input('Continue? [y/n] ')
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
        user_in = str(input("Do you want to run in interactive mode (i) or automatic (any key)? "))
        interactive = 'interactive' if user_in == 'i' else 'automatic'
    return interactive


def check_continue(user_continue=None):
    """
    Reads from input if user wants to continue.
    :param user_continue:  
    :return boolean:
    """
    while not user_continue:
        user_in = input('Next Step? Press enter to continue, "n" to stop ')
        user_continue = False if user_in == 'n' else True
    return user_continue


def select_grids(grid_file=GRID_DIR):
    """
    displays provided directory and user chooses from files in directory
    or parsing the .grid file accordingly
    :returns grid:
    """
    if os.path.isdir(grid_file):
        print('Grid Files in {g_dir} is:'.format(g_dir=grid_file))
        all_files = os.listdir(grid_file)
        for i, _file in enumerate(all_files):
            print('[{number}]   -   {name}'.format(number=i, name=_file))
        try:
            index = int(input('Select .grid file by number... '))
            # if integer can be casted without error and should be in limits
            if not 0 <= index < len(all_files):
                raise ValueError
        except ValueError as e:
            print('Not an integer in the correct range...')
            print(e)
        grid_file = os.path.join(GRID_DIR, all_files[index])
    if grid_file[-4:] == 'grid':
        grid_path = grid_file
    else:
        print('Oops. You have provided the wrong file!')
        raise FileNotFoundError
    return grid_path


def select_start(run_mode='random'):
    """
    Reads and assigns the mode for selecting the start value
    either static - always at lower left corner (0,2) or random for each episode
    :param run_mode:
    :return 'static' or 'random':
    """
    while not run_mode:
        run_mode = int(input("Select [0] for 'static' start at [0,0] or "
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
    """
    Read number of epsiodes as integer value from input
    :param episodes: Can take default value.
    :return int episodes:
    """
    while not episodes:
        episodes = int(input("Enter number of how many episodes to run... "))
        if episodes > 0:
            break
        else:
            print('Value cannot be negative!')
            episodes = None
            continue
    return episodes


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
                                  "The absolute difference of the values from the "
                                  "generated q-tables, leading to termination if "
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
