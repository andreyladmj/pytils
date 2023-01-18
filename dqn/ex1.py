import tensorflow as tf
import numpy as np
import gym
from matplotlib import pyplot as plt
from tensorflow.keras.models import load_model

env = gym.make("LunarLander-v2", render_mode='rgb_array')


class model(tf.keras.Model):
    def __init__(self):
        super().__init__()
        self.d1 = tf.keras.layers.Dense(256, activation='relu')
        self.d2 = tf.keras.layers.Dense(256, activation='relu')
        self.out = tf.keras.layers.Dense(4, activation=None)

    def call(self, input_data):
        x = self.d1(input_data)
        x = self.d2(x)
        x = self.out(x)
        return x

    def action_value(self, state):
        q_values = self.predict(state, verbose=0)
        return q_values


class experience():
    def __init__(self, buffer_size, state_dim):
        self.buffer_size = buffer_size
        self.pointer = 0
        self.state_mem = np.zeros((self.buffer_size, *state_dim), dtype=np.float32)
        self.action_mem = np.zeros(self.buffer_size, dtype=np.int32)
        self.next_state_mem = np.zeros((self.buffer_size, *state_dim), dtype=np.float32)
        self.reward_mem = np.zeros(self.buffer_size, dtype=np.int32)
        self.done_mem = np.zeros(self.buffer_size, dtype=np.bool)

    def add_exp(self, state, action, reward, next_state, done):
        idx = self.pointer % self.buffer_size
        self.state_mem[idx] = state
        self.action_mem[idx] = action
        self.reward_mem[idx] = reward
        self.next_state_mem[idx] = next_state
        self.done_mem[idx] = done
        self.pointer += 1

    def sample_exp(self, batch_size):
        max_mem = min(self.pointer, self.buffer_size)
        batch = np.random.choice(max_mem, batch_size, replace=False)
        state = self.state_mem[batch]
        action = self.action_mem[batch]
        reward = self.reward_mem[batch]
        next_state = self.next_state_mem[batch]
        done = self.done_mem[batch]
        return state, action, reward, next_state, done


class agent():
    def __init__(self):
        self.q_net = model()
        self.target_net = model()
        opt = tf.keras.optimizers.Adam(learning_rate=0.001)
        self.q_net.compile(optimizer=opt, loss='mse')
        self.target_net.compile(optimizer=opt, loss='mse')
        self.epsilon = 1.0
        self.epsilon_decay = 1e-3
        self.min_epsilon = 0.01
        self.memory = experience(buffer_size=1000000, state_dim=env.observation_space.shape)
        self.batch_size = 64
        self.gamma = 0.99
        self.replace = 100
        self.trainstep = 0
        self.action_space = [i for i in range(4)]

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            # action = env.action_space.sample()
            action = np.random.choice(self.action_space)

        else:
            state = np.array([state])
            action = self.q_net.action_value(state)
            action = np.argmax(action)

        return action

    def train(self):
        if self.memory.pointer < self.batch_size:
            return

        if self.trainstep % self.replace == 0:
            self.update_target()

        states, actions, rewards, next_states, dones = self.memory.sample_exp(self.batch_size)
        target = self.q_net.action_value(states)
        next_state_val = self.target_net.action_value(next_states)
        q_next = tf.math.reduce_max(next_state_val, axis=1, keepdims=True).numpy()
        # print("next state pred {}".format(next_state_val))
        q_target = np.copy(target)
        for i, d in enumerate(dones):
            if d:
                q_target[i, actions[i]] = rewards[i]

            else:
                # q_target[i, actions[i]] = rewards[i] + self.gamma * np.max(next_state_val[i])
                q_target[i, actions[i]] = rewards[i] + self.gamma * q_next[i]

        # print(states)
        # print(q_target)
        self.q_net.train_on_batch(states, q_target)
        self.update_epsilon()
        self.trainstep += 1

    def update_mem(self, state, action, reward, next_state, done):
        self.memory.add_exp(state, action, reward, next_state, done)

    def update_target(self):
        self.target_net.set_weights(self.q_net.get_weights())

    def update_epsilon(self):
        self.epsilon = self.epsilon - self.epsilon_decay if self.epsilon > self.min_epsilon else self.min_epsilon
        return self.epsilon

    def save_model(self):
        self.q_net.save("model.h5")
        self.target_net.save("target_model.h5")

    def load_model(self):
        self.q_net = load_model("model.h5")
        self.target_net = load_model("model.h5")


agentoo7 = agent()
steps = 500

for s in range(steps):
    done = False
    state, info = env.reset()
    total_reward = 0
    t = 0
    while not done:
        # env.render()
        action = agentoo7.act(state)
        # print(action)
        next_state, reward, done, _, _ = env.step(action)
        agentoo7.update_mem(state, action, reward, next_state, done)
        agentoo7.train()
        state = next_state
        total_reward += reward
        t += 1
        if done:
            print("total reward after {} episode is {} and epsilon is {}".format(s, total_reward, agentoo7.epsilon))


done = False
state, info = env.reset()
while not done:
    action = agentoo7.act(state)
    next_state, reward, done, _, _ = env.step(action)
    state = next_state
    plt.imshow(env.render())
    plt.show()
