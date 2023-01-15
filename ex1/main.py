import os, sys

import numpy as np

# sys.path.append(os.path.dirname(__file__))
from ex1.agent import Agent
from ex1.discrete_env import DiscreteEnv
from ex1.wmap import WMap

s = 1
wmap = WMap()
env = DiscreteEnv(wmap.start_pos, wmap.end_pos, wmap.P)
agentoo7 = Agent()


tries = [
    (True, 5, 10),
    (True, 10, 20),
    (False, 15, 30),
    (False, 20, 35),
    (False, 30, 40),
]
for add_random_actions, max_steps, steps in tries:
    for s in range(steps):

        done = False
        env.max_steps = max_steps
        state = env.reset()
        total_reward = 0
        rewards = []
        states = []
        actions = []

        while not done:
            # env.render()
            # add if action is possible
            action = agentoo7.act(state, add_random_actions=add_random_actions)

            next_state, reward, done, _ = env.step(action)
            rewards.append(reward)
            states.append(state)
            actions.append(action)
            state = next_state
            total_reward += reward
            # print("probs:", agentoo7.get_probs(state))
            # print("action:", env.actions[action])
            # print("current_pos:", env.current_pos, 'reward:', reward)
            # print("end_pos:", env.end_pos)
            # env.render()

            # if len(states) % 30 == 0:
            #     done = True
                # print("Iters:", len(states), "total_reward:", total_reward)
                # agentoo7.train(states, rewards, actions)
                # break

            if done:
                loses = agentoo7.train(states, rewards, actions)
                # print("total step for this episord are {}".format(t))
                print(f"total reward after {s} steps is {total_reward}, loses: {np.mean(loses)}")
                # plt.plot(loses)
                # plt.show()
                # env.render()

for i in range(10):
    action = agentoo7.act(state, add_random_actions=add_random_actions)
    next_state, reward, done, _ = env.step(action)
    rewards.append(reward)
    states.append(state)
    actions.append(action)
    state = next_state
    total_reward += reward
    print("probs:", agentoo7.get_probs(state))
    print("action:", env.actions[action])
    print("current_pos:", env.current_pos, 'reward:', reward)
    print("end_pos:", env.end_pos)
env.render()