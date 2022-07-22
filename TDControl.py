import numpy as np
import pygame
import random
import time
import config
from Agent import Agent
from Environment import Environment


class TDControl:
    """
    Implementation of temporal-difference reinforcement learning method.
    """
    def __init__(self, env, agent, gamma=1.0, eps=0.1, alpha=0.5, Q=None, PI=None):
        self.env = env
        self.agent = agent
        if Q is not None:
            self.Q = np.load(Q)
        else:
            self.Q = np.random.rand(config.WINDOW_HEIGHT, config.WINDOW_WIDTH, len(self.env.actions)) * -100
            self.Q[self.env.terminal] = 0

        if PI is not None:
            self.PI = np.load(PI)
        else:
            self.PI = self.env.actions[np.argmax(self.Q, axis=2)]
        self.gamma = gamma
        self.eps = eps
        self.alpha = alpha

    def getState(self):
        return self.agent.getX(), self.agent.getY()

    def target_policy(self, s):
        """
        Epsilon greedy policy having (1-eps)% chances to take current best action with respect to PI abd eps% chances
        to take random action. If greedy action is not present in possible actions, random action is then taken.
        """
        possible_a = self.env.possibleActions(s)
        greedy_a = self.PI[s]
        if np.random.rand() > self.eps and any((possible_a == greedy_a).all(1)):
            a = greedy_a
        else:
            a = random.choice(possible_a)

        return a

    def target_policy_non_greedy(self, s):
        """
        Evaluation policy returning greedy action if it is in possible actions or random action else.
        """
        possible_a = self.env.possibleActions(s)
        greedy_a = self.PI[s]
        if any((possible_a == greedy_a).all(1)):
            a = greedy_a
        else:
            a = random.choice(possible_a)

        return a

    def refreshFrame(self, CLOCK, fps=10):
        self.env.screen.fill(config.BLACK)
        self.env.draw()
        self.agent.draw()
        pygame.display.update()
        CLOCK.tick(fps)
        #time.sleep(3)

    def sarsa(self, CLOCK):
        """
        On-policy Temporal-Difference control method.
        """
        self.agent.restart()
        S = self.agent.getState()
        A = self.target_policy(S)
        a_map = self.env.mapAction(A)
        sa = S + (a_map,)
        #self.refreshFrame(CLOCK)

        while True:
            a_wind = self.env.applyWind(sa)
            self.agent.move(a_wind)
            #self.refreshFrame(CLOCK)

            if self.env.finish(S):
                break

            S = self.agent.getState()
            A = self.target_policy(S)
            a_map = self.env.mapAction(A)
            sa_prime = S + (a_map,)
            R = -1
            self.Q[sa] += self.alpha * (R + self.gamma * self.Q[sa_prime] - self.Q[sa])
            self.PI[sa[:-1]] = self.env.actions[np.argmax(self.Q[sa[:-1]])]
            sa = sa_prime

    def evaluate(self, CLOCK):
        """
        Evaluation of learned policy.
        """
        steps = 0
        self.agent.restart()
        S = self.agent.getState()
        A = self.target_policy(S)
        a_map = self.env.mapAction(A)
        sa = S + (a_map,)
        self.refreshFrame(CLOCK)

        while True:
            a_wind = self.env.applyWind(sa)
            self.agent.move(a_wind)
            self.refreshFrame(CLOCK)

            if self.env.finish(S):
                break

            S = self.agent.getState()
            A = self.target_policy_non_greedy(S)
            a_map = self.env.mapAction(A)
            sa = S + (a_map,)
            steps += 1

        return steps

    def save_params(self):
        np.save('train_params/PI.npy', self.PI)
        np.save('train_params/Q.npy', self.Q)