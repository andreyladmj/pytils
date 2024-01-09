
import os
import gym
import numpy as np

from dqn.ex2.agent import DQNAgent

env = gym.make('CartPole-v0')
state_size = env.observation_space.shape[0]
action_size = env.action_space.n
batch_size = 32
n_episodes = 1000
output_dir = 'model_output/'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

agent = DQNAgent(state_size, action_size)

for e in range(n_episodes):
    state, _ = env.reset()
    state = np.reshape(state, [1, state_size])
    done = False
    time = 0
    while not done:
#         env.render()
        action = agent.act(state)
        next_state, reward, done, _, _ = env.step(action)
        # print("action:", action, "reward:", reward)

        reward = reward if not done else -10
        next_state = np.reshape(next_state, [1, state_size])
        agent.remember(state, action, reward, next_state, done)
        state = next_state

        if done:
            print("episode: {}/{}, score: {}, e: {:.2}".format(e, n_episodes-1, time, agent.epsilon))
            # for i, (state, action, reward, next_state, done) in enumerate(agent.memory):
            #     print(i, action, reward, done)

        time += 1

    if len(agent.memory) > batch_size:
        agent.train(batch_size)

    if e % 50 == 0:
        agent.save_weights(output_dir + "weights_" + '{:04d}'.format(e) + ".hdf5")
        agent.save(output_dir + "" + '{:04d}'.format(e) + ".hdf5")