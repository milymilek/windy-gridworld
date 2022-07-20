import numpy as np
import pygame
import random

import utils


class Vehicle(pygame.sprite.Sprite):
    def __init__(self, board):
        super().__init__()
        self.rect = pygame.Rect(0, 0, utils.BLOCK_SIZE, utils.BLOCK_SIZE)
        self.image = pygame.image.load("img/ball.png")
        self.board = board
        self.velocity = np.array([0, 0])

    def addVelocity(self, v):
        self.velocity += v

    def move(self):
        self.rect.move_ip(self.velocity[1] * utils.BLOCK_SIZE, self.velocity[0] * utils.BLOCK_SIZE)

    def restart(self):
        self.velocity[:] = 0
        #self.velocity[0] = 1
        #self.velocity[1] = 1
        start = random.choice(self.board.track["start"])
        #print("new start: ", start.xx, ", ", start.yy)
        self.rect.y = start.xx * utils.BLOCK_SIZE
        self.rect.x = start.yy * utils.BLOCK_SIZE

    def draw(self):
        pygame.draw.rect(self.board.screen, [0, 200, 200], self.rect)

    def getX(self):
        return self.rect.y // utils.BLOCK_SIZE

    def getY(self):
        return self.rect.x // utils.BLOCK_SIZE

    def finish(self):
        meta_upper_x = min([c.xx for c in self.board.track['meta']])
        meta_lower_x = max([c.xx for c in self.board.track['meta']])
        meta_y = max([c.yy for c in self.board.track['meta']])
        return (meta_upper_x <= self.getX() <= meta_lower_x) and self.getY() >= meta_y

        # if any(self.rect == c for c in self.board.track["meta"]):
        #     return True
        # else:
        #     return False

    def hitWall(self):
        return not ((0 <= self.getX() <= self.board.n-1) and (0 <= self.getY() <= self.board.n-1)) or \
                    any(self.rect == c for c in self.board.track["wall"])
