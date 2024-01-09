import random
import numpy as np
from tensorflow.python.keras import Sequential
from tensorflow.python.keras.layers import Dense
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import tensorflow as tf

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        # self.epsilon_decay = 0.915
        self.epsilon_min = 0.01
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        model = Sequential(name="l1")
        model.add(Dense(32, activation='relu', input_dim=self.state_size, name="l2"))
        model.add(Dense(32, activation='relu', name="l3"))
        model.add(Dense(self.action_size, activation='linear', name="l4"))
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)

        # states = []
        # targets = []

        # print("self.memory:",len(self.memory),'minibatch:',len(minibatch))
        for state, action, reward, next_state, done in minibatch:
            target = reward  # if done
            # if not done:
            #     target = (reward + self.gamma * np.amax(self.model.predict(next_state, verbose=0)[0]))

            # print("state:", state, "target:", target)
            target_f = self.model.predict(state, verbose=0)
            target_f[0][action] = target
            # print("target_f:", target_f)
            self.model.fit(state, target_f, epochs=1, verbose=0)
            # states.append(state)
            # targets.append(target_f[0])

        # self.model.fit(np.array(states), np.array(targets), epochs=1, verbose=0)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state, verbose=0)
        return np.argmax(act_values[0])

    def save(self, name):
        self.model.save(name)

        # with tf.Session() as sess:
        #     tf.train.Saver(tf.trainable_variables()).save(sess, 'models/my-model')

    def save_weights(self, name):
        self.model.save_weights(name)

    def load(self, name):
        self.model.load_weights(name)