## Methods of AI Programming Task

Read a gridworld and apply policy iteration according to user input.
Usage: 
`python GridWorld.py -h` for help.

 
GridWorld \[options\]

Necessary are the positional arguments...

positional arguments:
  grid_file             path to input .grid file

optional arguments:
  -h, --help            show this help message and exit
  -i ITER, --iter ITER  number of iterations performed by the policy iteration
  -s, --step            manual iteration for policy iteration
  -g GAMMA, --gamma GAMMA
                        discount value gamma

Dependencies:
+ python3 v3.6.4
+ argparse v1.1
+ numpy v1.13.3

Constants.py - contains static global variables.
Evaluator.py - works with the grid; iterates over it and improves policy

![Maze Westworld](https://images.duckduckgo.com/iu/?u=https%3A%2F%2Fi.redd.it%2Ftz1bngoyiw1y.jpg&f=1)