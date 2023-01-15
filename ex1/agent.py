import random

import tensorflow as tf
import numpy as np
import gym
import tensorflow_probability as tfp

epsilon = 0.1

class Model(tf.keras.Model):
    def __init__(self):
        super().__init__()
        self.d1 = tf.keras.layers.Dense(30, activation='relu')
        self.d2 = tf.keras.layers.Dense(30, activation='relu')
        self.out = tf.keras.layers.Dense(4, activation='softmax')

    def call(self, input_data):
        x = tf.convert_to_tensor(input_data)
        x = self.d1(x)
        x = self.d2(x)
        x = self.out(x)
        return x


class Agent():
    def __init__(self):
        self.model = Model()
        self.opt = tf.keras.optimizers.Adam(learning_rate=0.001)
        self.gamma = 1

    def get_probs(self, state):
        probs = [p.numpy() for p in self.model(np.array([state]))[0]]
        return probs

    def act(self, state):
        # if np.random.uniform(0,1) < epsilon:
        #     return random.choice([0,1,2,3])

        prob = self.model(np.array([state]))
        dist = tfp.distributions.Categorical(probs=prob, dtype=tf.float32)
        action = dist.sample()
        return int(action.numpy()[0])

    def a_loss(self, prob, action, reward):
        dist = tfp.distributions.Categorical(probs=prob, dtype=tf.float32)
        log_prob = dist.log_prob(action)
        loss = -log_prob * reward
        return loss

    def fail_train(self, states, rewards, actions):
        self.train(states, rewards, actions)

    def train(self, states, rewards, actions):
        sum_reward = 0
        discnt_rewards = []
        rewards.reverse()
        for r in rewards:
            sum_reward = r + self.gamma * sum_reward
            discnt_rewards.append(sum_reward)
        discnt_rewards.reverse()

        for state, reward, action in zip(states, discnt_rewards, actions):
            with tf.GradientTape() as tape:
                p = self.model(np.array([state]), training=True)
                loss = self.a_loss(p, action, reward)
            grads = tape.gradient(loss, self.model.trainable_variables)
            self.opt.apply_gradients(zip(grads, self.model.trainable_variables))
