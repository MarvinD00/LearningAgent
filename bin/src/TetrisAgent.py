import numpy as np
import torch
import random
from . import TetrisEnvironment as te
from collections import deque
from .Model import Linear_QNet, QTrainer

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LEARNING_RATE = 0.001
EPSILON_START = 1000
EPSILON_END = 20

class TetrisAgent:
	
	def __init__(self):
		self.number_of_games = 0
		self.epsilon = 0
		self.gamma = 0.4
		self.model = Linear_QNet(360,256,4)
		self.trainer = QTrainer(self.model, gamma=self.gamma, learning_rate=LEARNING_RATE)
		self.memory = deque(maxlen=MAX_MEMORY)
		self.environment = te.TetrisEnvironment()


	def get_state(self):
		return self.environment.get_state()
	
	def remember(self, state, action, reward, next_state, done):
		self.memory.append((state, action, reward, next_state, done))

	def train_long_memory(self):
		if (len(self.memory) > BATCH_SIZE):
			mini_sample = random.sample(self.memory,BATCH_SIZE)
		else:
			mini_sample = self.memory
		
		states, actions, rewards, next_states, dones = zip(*mini_sample)
		self.trainer.train_step(states, actions, rewards, next_states, dones)

	def train_short_memory(self, state, action, reward, next_state, done):
		self.trainer.train_step(state, action, reward, next_state, done)

	def get_action(self, state):
		self.epsilon = EPSILON_START - self.number_of_games + EPSILON_END
		final_move = ...
		if((random.randint(0,EPSILON_START)) < self.epsilon):
			move = random.randint(0,3)
		else:
			state0 = torch.tensor(state, dtype=torch.float)
			prediction = self.model(state0)
			move = torch.argmax(prediction).item()

		return move

	def train(self):
		plot_avg_rewards = []
		plot_mean_avg_rewards = []
		total_avg_rewards = 0
		record = 0
		game = te.TetrisEnvironment()
		total_rewards = []
		while True:
			old_state = self.get_state()

			final_move = self.get_action(old_state)

			reward, done, score = game.step(final_move)
			total_rewards.append(reward)
			new_state = self.get_state()

			self.train_short_memory(old_state, final_move, reward, new_state, done)

			self.remember(old_state, final_move, reward, new_state, done)

			if done:
				game.reset()
				self.number_of_games += 1
				self.train_long_memory()

				if score > record:
					record = score
					self.model.save()

				avg_reward = sum(total_rewards)/len(total_rewards)
				print('Game', self.number_of_games, 'Score', score, 'Record:', record, end="")
				print(" avg_reward: " + str(avg_reward))
				total_rewards = []

				plot_avg_rewards.append(avg_reward)
				total_avg_rewards += avg_reward
				mean_avg_rewards = total_avg_rewards / self.number_of_games
				plot_mean_avg_rewards.append(mean_avg_rewards)
				plot(plot_avg_rewards, plot_mean_avg_rewards)