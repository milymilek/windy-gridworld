import pygame

import utils


class Cell(pygame.Rect):
    """
    Representation of single Rect object on board.
    Coordinates of cell are reversed because of reverse ordering in pygame lib.
    """
    def __init__(self, board, x, y, track):
        super().__init__(x * utils.BLOCK_SIZE, y * utils.BLOCK_SIZE, utils.BLOCK_SIZE, utils.BLOCK_SIZE)
        self.board = board
        self.track = track
        self.xx = y
        self.yy = x

    def __repr__(self):
        return f'Cell({0}, {self.yy}, {self.xx}, {self.track})'

    def setBoard(self, board):
        self.board = board
