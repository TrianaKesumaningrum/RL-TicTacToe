from abc import ABC, abstractmethod
import os
import pickle
import collections
import numpy as np
import random


class Learner(ABC):
    """
    Parent class for Q-learning and SARSA agents.
    """
    def __init__(self, alpha, gamma, eps, eps_decay=0.):
        # Agent parameters
        self.alpha = alpha
        self.gamma = gamma
        self.eps = eps
        self.eps_decay = eps_decay
        # Possible actions correspond to the set of all x,y coordinate pairs
        self.actions = [(i, j) for i in range(4) for j in range(4)]
        # Initialize Q values to 0 for all state-action pairs.
        self.Q = {action: collections.defaultdict(int) for action in self.actions}
        # Keep a list of reward received at each episode
        self.rewards = []

    def get_action(self, s):
        """
        Select an action given the current game state.

        Parameters
        ----------
        s : string
            state
        """
        # Only consider the allowed actions (empty board spaces)
        possible_actions = [a for a in self.actions if s[a[0] * 4 + a[1]] == '-']
        if random.random() < self.eps:
            # Random choose.
            action = random.choice(possible_actions)
        else:
            # Greedy choose.
            values = np.array([self.Q[a][s] for a in possible_actions])
            ix_max = np.where(values == np.max(values))[0]
            action = possible_actions[np.random.choice(ix_max)]

        # update epsilon; geometric decay
        self.eps *= (1. - self.eps_decay)

        return action

    def save(self, path):
        """ Pickle the agent object instance to save the agent's state. """
        if os.path.isfile(path):
            os.remove(path)
        with open(path, 'wb') as f:
            pickle.dump(self, f)

    @abstractmethod
    def update(self, s, s_, a, a_, r):
        pass


class Qlearner(Learner):
    """
    A class to implement the Q-learning agent.
    """
    def __init__(self, alpha, gamma, eps, eps_decay=0.):
        super().__init__(alpha, gamma, eps, eps_decay)

    def update(self, s, s_, a, a_, r):
        """
        Perform the Q-Learning update of Q values.

        Parameters
        ----------
        s : string
            previous state
        s_ : string
            new state
        a : (i,j) tuple
            previous action
        a_ : (i,j) tuple
            new action. NOT used by Q-learner!
        r : int
            reward received after executing action "a" in state "s"
        """
        if s_ is not None:
            possible_actions = [action for action in self.actions if s_[action[0] * 4 + action[1]] == '-']
            Q_options = [self.Q[action][s_] for action in possible_actions]
            self.Q[a][s] += self.alpha * (r + self.gamma * max(Q_options) - self.Q[a][s])
        else:
            self.Q[a][s] += self.alpha * (r - self.Q[a][s])

        self.rewards.append(r)


class SARSAlearner(Learner):
    """
    A class to implement the SARSA agent.
    """
    def __init__(self, alpha, gamma, eps, eps_decay=0.):
        super().__init__(alpha, gamma, eps, eps_decay)

    def update(self, s, s_, a, a_, r):
        """
        Perform the SARSA update of Q values.

        Parameters
        ----------
        s : string
            previous state
        s_ : string
            new state
        a : (i,j) tuple
            previous action
        a_ : (i,j) tuple
            new action
        r : int
            reward received after executing action "a" in state "s"
        """
        if s_ is not None:
            self.Q[a][s] += self.alpha * (r + self.gamma * self.Q[a_][s_] - self.Q[a][s])
        else:
            self.Q[a][s] += self.alpha * (r - self.Q[a][s])

        self.rewards.append(r)

# You should include the Game class and necessary functions from previous responses for the complete functionality.
