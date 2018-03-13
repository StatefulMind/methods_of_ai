## Methods of AI Programming Task

Read a gridworld file and apply policy iteration or Q-learning.

Read user input via dialogue UI from the commandline and apply specified values.
Either apply learning iteratively and interactive or automatic until convergence 
has been reached or amount of episodes reached

Usage:
Policy Iteration:
`python QLearn.py`

Q-Learner:
`python QLearn.py`


Dependencies:
+ python3 v3.6.4 
+ numpy v1.13.3 
+ pandas v0.20.2

Constants.py    - contains static global variables.

Evaluator.py    - works with the grid; iterates over it and improves policy

Grid.py         - contains grid class that constructs the grid, evaluation and policy grid with all according methods

GridField.py    - contains class-structure for the different types of fields

Learner.py    - learns from grid and improves policy by applying q-learning

GridWorld.py - contains executable main function and user dialogue that handles all inputs and runs specified methods

QLearn.py    - contains executable main function and calls grid and UI functions 

![Maze Westworld](https://images.duckduckgo.com/iu/?u=https%3A%2F%2Fi.redd.it%2Ftz1bngoyiw1y.jpg&f=1)