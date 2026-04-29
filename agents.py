import numpy as np

class Agent:
    def __init__(self, env, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.env = env
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.actions = env.actions
        self.Q = np.zeros((env.height, env.width, len(self.actions)))

    def choose_action(self, state):
        if np.random.rand() < self.epsilon:
            return np.random.choice(self.actions)
        else:
            r, c = state
            values = self.Q[r, c, :]
            # to break ties randomly:
            max_val = np.max(values)
            best_actions = np.where(values == max_val)[0]
            return np.random.choice(best_actions)

class QLearningAgent(Agent):
    def update(self, state, action, reward, next_state, done):
        r, c = state
        nr, nc = next_state
        if done:
            td_target = reward
        else:
            best_next_action = np.argmax(self.Q[nr, nc, :])
            td_target = reward + self.gamma * self.Q[nr, nc, best_next_action]
        td_error = td_target - self.Q[r, c, action]
        self.Q[r, c, action] += self.alpha * td_error

class SarsaAgent(Agent):
    def update(self, state, action, reward, next_state, next_action, done):
        r, c = state
        nr, nc = next_state
        if done:
            td_target = reward
        else:
            td_target = reward + self.gamma * self.Q[nr, nc, next_action]
        td_error = td_target - self.Q[r, c, action]
        self.Q[r, c, action] += self.alpha * td_error
