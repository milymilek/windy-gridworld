import numpy as np
import pygame
import random
import time

import utils
from Vehicle import Vehicle



class Agent:
    def __init__(self, board, gamma=1.0, eps=0.1):
        self.board = board
        self.vehicle = Vehicle(board)
        self.actions = np.array([np.array([x, y]) for x in range(-1, 2) for y in range(-1, 2)])
        self.actions_map = {(a[0], a[1]): i for i, a in enumerate(self.actions)}
        self.Q = np.random.rand(utils.WINDOW_SIZE // utils.BLOCK_SIZE, utils.WINDOW_SIZE // utils.BLOCK_SIZE,
                                utils.MAX_VEL+1, utils.MAX_VEL+1, len(self.actions)) * -100
        self.C = np.zeros_like(self.Q)
        self.PI = self.actions[np.argmax(self.Q, axis=4)]
        self.gamma = gamma
        self.eps = eps
        #self.eval_history = open("eval_history.txt", "w")

        '''print(f'actions: {self.actions} \nactions_map: {self.actions_map} \n state_track: {self.state_track} \n'
              f'state_track_map: {self.state_track_map} \nstate_velocity: {self.state_velocity} \nstate_velo_map: {self.state_velocity_map}'
              f'\nQ shape: {self.Q.shape} \nPI shape: {self.PI.shape}')'''

    def getState(self):
        return self.vehicle.getX(), self.vehicle.getY(), self.vehicle.velocity[0], self.vehicle.velocity[1]

    def mapAction(self, a):
        return np.where((self.actions[:, 0] == a[0]) & (self.actions[:, 1] == a[1]))[0][0]

    def mapStateAction(self, s, a):
        return self.state_track_map[(s[0], s[1])], self.state_velocity_map[(s[2], s[3])], self.actions_map[(a[0], a[1])]

    def possibleActions(self):
        new_vel = self.actions + self.vehicle.velocity
        #print("velo: ", self.vehicle.velocity)
        #print("new vel: \n", new_vel)
        possible_a = np.where((new_vel[:, 0] < utils.MAX_VEL) & (new_vel[:, 0] >= 0) &
                             (new_vel[:, 1] < utils.MAX_VEL) & (new_vel[:, 1] >= 0) &
                             (new_vel.any(axis=1)))
        #print("possible a: \n", possible_a)
        return self.actions[possible_a]

    def b(self, s):
        possible_a = self.possibleActions()
        greedy_a = self.PI[s]
        if np.random.rand() > self.eps and any((possible_a == greedy_a).all(1)):
            a = greedy_a
        else:
            a = random.choice(possible_a)

        b_a = self.b_a(a, possible_a, greedy_a)

        return a, b_a

    def target_policy(self, s):
        possible_a = self.possibleActions()
        greedy_a = self.PI[s]
        if any((possible_a == greedy_a).all(1)):
            return greedy_a
        else:
            return random.choice(possible_a)

    def b_a(self, a, possible_a, greedy_a):
        num_a = len(possible_a)

        if greedy_a in possible_a:
            if np.array_equal(a, greedy_a):
                prob = 1 - self.eps + self.eps / num_a
            else:
                prob = self.eps / num_a
        else:
            prob = 1 / num_a

        return prob

    def refreshFrame(self, CLOCK, fps=1000):
        self.board.screen.fill(utils.BLACK)
        self.board.draw()
        self.vehicle.draw()
        pygame.display.update()
        CLOCK.tick(fps)
        #time.sleep(1)

    def mc_control(self, CLOCK):
        G = 0
        W = 1
        alive = True
        history = []
        self.vehicle.restart()

        while alive:
            S = self.getState()
            A, b_A = self.b(S)
            self.vehicle.addVelocity(A)
            self.vehicle.move()

            if self.vehicle.finish():
                alive = False
                R = -1
            elif self.vehicle.hitWall():
                self.vehicle.restart()
                R = -1
            else:
                R = -1

            G += R
            history.append((S, A, R, b_A))

        print(f"Return: {G}")
        G = 0

        for s, a, r, b_a in history[::-1]:
            a_map = self.mapAction(a)
            sa = s + (a_map,)
            G = self.gamma * G + r
            self.C[sa] += W
            self.Q[sa] = self.Q[sa] + (W / self.C[sa]) * (G - self.Q[sa])
            self.PI[s] = self.actions[np.argmax(self.Q[s])]


            if not (a[0] == self.PI[s][0] and a[1] == self.PI[s][1]):
                break
            else:
                print("back")

            W /= b_a


    def evaluate(self, CLOCK):
        G = 0
        alive = True
        self.vehicle.restart()

        while alive:
            self.refreshFrame(CLOCK)

            S = self.getState()
            A = self.target_policy(S)
            self.vehicle.addVelocity(A)
            self.vehicle.move()

            if self.vehicle.finish():
                self.refreshFrame(CLOCK)
                alive = False
                R = 0
            elif self.vehicle.hitWall():
                self.refreshFrame(CLOCK)
                self.vehicle.restart()
                R = -1
            else:
                R = -1

            G += R

        print(f"Return: {G}")
        self.eval_history.write(f'{G}\n')

    def save_params(self):
        np.save('train_params/PI.npy', self.PI)
        np.save('train_params/Q.npy', self.Q)