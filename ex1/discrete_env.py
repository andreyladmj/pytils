import math
import matplotlib.pyplot as plt

import numpy as np


class DiscreteEnv:
    def __init__(self, start_pos, end_pos, P):
        self.start_pos = start_pos
        self.current_pos = start_pos
        self.end_pos = end_pos
        self.P = P
        self.actions = {0: 'top', 1: 'left', 2: 'right', 3: 'bottom'}

    def render(self):
        arr = np.copy(self.P)
        arr[self.current_pos] = 2
        plt.imshow(arr)
        plt.show()

    def reset(self):
        self.current_pos = self.start_pos
        return self.get_state()

    def get_vector(self):
        return (self.end_pos[0] - self.current_pos[0], self.end_pos[1] - self.current_pos[1])

    def get_state(self):
        return self.current_pos + self.get_vector()

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

        dist_to_start = self.get_distance(next_pos, self.start_pos)
        dist_to_end = self.get_distance(next_pos, self.end_pos)
        reward = 25 + dist_to_start - dist_to_end

        done = next_pos == self.end_pos

        # if self.P[next_pos] == 1:
        #     reward -= 1

        self.current_pos = next_pos

        return self.get_state(), reward, done, {}
