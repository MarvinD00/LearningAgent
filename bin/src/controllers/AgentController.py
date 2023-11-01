import numpy as np
import pandas as pd
import pygame
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import random

# define the model
model = Sequential()
model.add(Dense(32, input_shape=(10,18), activation="relu"))
model.add(Dense(32, activation="relu"))
model.add(Dense(18, activation="linear")) 
model.compile(loss="mse", optimizer="adam", metrics=["accuracy"])

# define the agent
class Agent:

    def __init__(self, env):
        self.is_training = True
        self.env = env
        self.memory = []
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
        self.batch_size = 32
        self.train_start = 1000

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.choice(self.env.action_space)
        else:
            return np.argmax(model.predict(state))

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train(self):
        if len(self.memory) < self.train_start:
            return
        batch_size = min(self.batch_size, len(self.memory))
        mini_batch = random.sample(self.memory, batch_size)
        update_input = np.zeros((batch_size, 10, 18))
        update_target = np.zeros((batch_size, 10, 18))
        
        for i in range(batch_size):
            state, action, reward, next_state, done = mini_batch[i]
            target = reward

            if not done:
                target = (reward + self.gamma * np.amax(model.predict(next_state)))

            update_input[i] = state
            update_target[i] = model.predict(state)
            position = np.where(self.env.action_space == action)[0]
            update_target[i][position] = target

        model.fit(update_input, update_target, batch_size=batch_size, epochs=1, verbose=0)

        # Decay epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        
    def load(self, name):
        model.load_weights(name)

    def save(self, name):
        model.save_weights(name)
    
    def run(self):
        EPISODES = 1000
        for e in range(EPISODES):
            state = self.env.reset()
            state = np.reshape(state, [1, 10, 18])
            print(state.shape) 
            done = False
            i = 0
            while not done:
                self.env.render()
                action = self.act(state)
                next_state, reward, done = self.env.step(action)
                next_state = np.reshape(next_state, [1, 10, 18])
                if not done or i == self.env._max_episode_steps - 1:
                    reward = reward
                else:
                    reward = -100
                self.remember(state, action, reward, next_state, done)
                state = next_state
                i += 1
    
            print("episode: {}/{}, score: {}, e: {:.2}".format(e, EPISODES, i, self.epsilon))
            if len(self.memory) > self.train_start:
                self.train()
            if e % 50 == 0:
                self.save("weights.h5")
            
