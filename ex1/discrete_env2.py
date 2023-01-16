from random import randint

import math
import matplotlib.pyplot as plt

import numpy as np


class DiscreteEnv2:
    def __init__(self, start_pos, end_pos, P):
        self.start_pos = start_pos
        self.current_pos = start_pos
        self.end_pos = end_pos
        self.origin_P = P
        self.P = P
        self.max_steps = 50
        self.i = 0
        self.actions = {0: 'top', 1: 'left', 2: 'right', 3: 'bottom'}

    def render(self):
        plt.imshow(self.P)
        plt.show()

    def normalize_state(self, state):
        max_distance = self.get_distance((0,0), (self.P.shape[0], self.P.shape[1]))
        state = list(state)
        state[0] /= self.P.shape[0]
        state[1] /= self.P.shape[1]
        state[2] /= self.P.shape[0]
        state[3] /= self.P.shape[1]
        state[4] /= max_distance
        return state

    def reset(self):
        self.P = np.copy(self.origin_P)
        self.start_pos = (randint(0, self.P.shape[0]-1), randint(0, self.P.shape[1]-1))
        self.current_pos = self.start_pos
        self.i = 0
        self.end_pos = (randint(0, self.P.shape[0]-1), randint(0, self.P.shape[1]-1))
        self.P[self.start_pos] = 3
        self.P[self.end_pos] = 4
        return self.get_state()

    def get_vector(self):
        return (self.end_pos[0] - self.current_pos[0], self.end_pos[1] - self.current_pos[1])

    def get_state(self):
        d = self.get_distance(self.current_pos, self.end_pos)
        return self.current_pos + self.get_vector() + tuple([d])

    def get_distance(self, p1, p2):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def get_next_position(self, action):
        x, y = self.current_pos
        if action == 1 and y >= 1: return (x, y - 1)
        if action == 0 and x >= 1: return (x - 1, y)
        if action == 3 and x < self.P.shape[0] - 1: return (x + 1, y)
        if action == 2 and y < self.P.shape[1] - 1: return (x, y + 1)
        return (x, y)

    def step(self, action):
        next_pos = self.get_next_position(action)
        reward = -1

        done = next_pos == self.end_pos

        # if self.P[next_pos] == 1:
        #     reward -= 1

        self.i += 1
        self.current_pos = next_pos
        self.P[self.current_pos] = 2

        if done:
            reward += 100

        if not done and self.i == self.max_steps:
            # reward = 25 #+ dist_to_start - dist_to_end
            done = True

        return self.get_state(), reward, done, {}
