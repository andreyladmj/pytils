import numpy as np

actions = [0,1,2,3,4,5,6,7,8]

rewards = np.array([[0,1,0,0,0,0,0,0,0],
                    [1,0,1,0,1,0,0,0,0],
                    [0,0,0,0,0,0,1,0,0],
                    [0,0,0,0,0,0,0,1,0],
                    [0,0,1,0,0,0,0,0,0],
                    [0,0,0,1,0,0,0,1,0],
                    [0,0,0,0,1,0,1,0,1],
                    [0,0,0,0,0,0,0,1,0]])

state_to_location = dict((state,location) for location, state in location_to_state.items())

gamma = 0.75 # Discount factor
alpha = 0.9 # Learninng rate

class QAgent:
    def __init__(self, alpha, gamma, location_to_state, actions, rewards, state_to_location, Q):
        self.gamma = gamma
        self.alpha = alpha

        self.location_to_state = location_to_state
        self.actions = actions
        self.rewards = rewards
        self.state_to_location = state_to_location

        self.Q = Q

    def training(self, start_location, end_location, iterations):
        rewards_new = np.copy(self.rewards)

        ending_state = self.location_to_state[end_location]
        rewards_new[ending_state, ending_state] = 999

        for i in range(iterations):
            current_state = np.random.randint(0,9)
            playable_actions = []

            for j in range(9):
                if rewards_new[current_state, j] > 0:
                    playable_actions.append(j)

        next_state = np.random.choice(playable_actions)

        TD = rewards_new[current_state, next_state] + self.gamma * self.Q[next_state, np.argmax(self.Q[next_state,])] - self.Q[current_state, next_state]

        self.Q[current_state, next_state] += self.alpha * TD

    route = [start_location]
    next_location = start_location

    self.get_