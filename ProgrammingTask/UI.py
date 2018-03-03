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
    """Checks if dependencies are met and imported packages have the right version
    exits script if requirements are not met"""
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
        print('Looks like you are not running the required {invalid} version !'
              '------------------------------------------------------------'
              'Please refer to the README and check the dependencies...'.format(invalid=invalid))
        sleep(1)
        print('EXITING NOW.')
        sys.exit(1)


def check_running():
    """Checks if the user wants to continue running the program
    if user enters n/N/No/NO False will be returned that leads to termination of script
    :returns running boolean:"""
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


def check_mode():
    while True:
        run_mode = int(input('Select [0] for manual run or [1] for automatic run... '))
        if run_mode == 0 or run_mode == 1:
            break
        else:
            print('Selection not in range')
            continue
    return run_mode


def select_grids(grid_file=GRID_DIR):
    """displays provided directory and user chooses from files in directory
    or parsing the .grid file accordingly
    :returns grid: """
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


def select_start():
    while True:
        run_mode = int(input("Select [0] for 'static' start at [0,0] or "
                             "[1] for 'random' starting points... "))
        if run_mode == 0 or run_mode == 1:
            run_mode = 'static' if run_mode == 0 else 'random'
            break
        else:
            print('Selection not in range')
            continue
    return run_mode


def select_epsilon():
    while True:
        epsilon = float(input("Select a value for the {epsilon} between 0..1 \n"
                            "where 0 --> greedy run and 1 --> random run... ".format(epsilon='\u03B5')))
        if 0 <= epsilon <= 1:
            break
        else:
            print('Value is not in range!')
            continue
    return epsilon


def run_manual(grid):
    pass


def run_automatic(grid):
    pass