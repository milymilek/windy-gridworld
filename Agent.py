import numpy as np
import pygame
import random
import time
import config


class Agent(pygame.sprite.Sprite):
    """
    Representation of object which tries to find optimal policy.
    x and y coordinates are swapped because of reverse notation in pygame library.
    """
    def __init__(self, board):
        super().__init__()
        self.agent = pygame.Rect(0, 0, config.BLOCK_SIZE, config.BLOCK_SIZE)
        self.board = board

    def getX(self):
        return self.agent.y // config.BLOCK_SIZE

    def getY(self):
        return self.agent.x // config.BLOCK_SIZE

    def getState(self):
        return self.getX(), self.getY()

    def draw(self):
        pygame.draw.rect(self.board.screen, [0, 200, 200], self.agent)

    def move(self, a):
        self.agent.move_ip(a[1] * config.BLOCK_SIZE, a[0] * config.BLOCK_SIZE)

    def restart(self):
        self.agent.y = config.START_STATE[0] * config.BLOCK_SIZE
        self.agent.x = config.START_STATE[1] * config.BLOCK_SIZE