import os, sys

sys.path.append(os.path.dirname(__file__))

from ex1.agent import Agent
from ex1.discrete_env import DiscreteEnv
from ex1.wmap import WMap

wmap = WMap()
env = DiscreteEnv(wmap.start_pos, wmap.end_pos, wmap.P)

agentoo7 = Agent()
steps = 500
s = 1
for s in range(steps):

    done = False
    state = env.reset()
    total_reward = 0
    rewards = []
    states = []
    actions = []

    while not done:
        # env.render()
        action = agentoo7.act(state)
        # print("probs:", agentoo7.get_probs(state))
        # print("action:", env.actions[action])

        next_state, reward, done, _ = env.step(action)
        rewards.append(reward)
        states.append(state)
        actions.append(action)
        state = next_state
        total_reward += reward
        # env.render()
        # print("current_pos:", env.current_pos, 'reward:', reward)

        # if len(states) % 30 == 0:
        #     done = True
            # print("Iters:", len(states), "total_reward:", total_reward)
            # agentoo7.train(states, rewards, actions)
            # break

        if done:
            agentoo7.train(states, rewards, actions)
            # print("total step for this episord are {}".format(t))
            print(f"total reward after {s} steps is {total_reward}")
            # env.render()