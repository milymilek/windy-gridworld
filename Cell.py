import pygame
import config


class Cell(pygame.Rect):
    """
    Representation of single Rect object on board.
    Coordinates of cell are reversed because of reverse ordering in pygame lib.
    """
    def __init__(self, board, x, y, track):
        super().__init__(x * config.BLOCK_SIZE, y * config.BLOCK_SIZE, config.BLOCK_SIZE, config.BLOCK_SIZE)
        self.board = board
        self.xx = y
        self.yy = x

    def __repr__(self):
        return f'Cell({0}, {self.yy}, {self.xx})'

    def setBoard(self, board):
        self.board = board
