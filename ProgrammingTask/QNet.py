import tensorflow as tf
import numpy as np
import gym


class QNet:
    '''
    Class that utilizes tensorflow datagraph to apply Q-learning to the given
    gridworld environment
    '''
    def __init__(self, grid, learning_rate=0.99, epsilon=0.1, episodes=2000):
        self._grid = grid
        self._learning_rate = learning_rate
        self._epsilon = epsilon
        self._episodes = episodes
        self._action_no = 4
        

    def make_dataflowgraph(self):
        tf.reset_default_graph()
        # shape is all possible input fields
        field_shape = self._grid.shape[0] * self._grid.shape[1]
        inputs = tf.placeholder(shape=[1, field_shape], dtype=tf.float32)
        # shape is all possible 4 directions - initial distribution from 0 to 0.01
        weights = tf.Variable.(tf.random_uniform([field_shape, 4], 0, 0.01))

    def run_dfg(self):
        for episode in range(self._episodes):
            tf.initialize_all_variables()

    def print(self):
        print(self._grid)
