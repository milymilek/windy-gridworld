import random
import pygame
import numpy as np

import config
from Cell import Cell


class Environment:
    """
    Class defining place where actions are taken by some objects.
    """
    def __init__(self, screen, width, height):
        self.screen = screen
        self.cells = []
        self.width = width
        self.height = height
        self.start = config.START_STATE
        self.terminal = config.TERMINAL_STATE
        self.wind = {0: 0, 1: 0, 2: 0, 3: -1, 4: -1, 5: -1, 6: -2, 7: -2, 8: -1, 9: 0}
        self.actions = np.array([[1, 0], [0, 1], [-1, 0], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]])

    def mapAction(self, a):
        """
        Get index of given action.

        ----------
        Parameters:
            a : np.array()

        -------
        Returns:
            int
                Matching index of action.
        """
        return np.where((self.actions[:, 0] == a[0]) & (self.actions[:, 1] == a[1]))[0][0]

    def createGrid(self):
        for x in range(0, self.width):
            for y in range(0, self.height):
                self.cells.append(Cell(self, x, y, False))

    def draw(self):
        """
        Draw grid and mark terminal state.
        """
        for c in self.cells:
            if (c.xx, c.yy) == self.terminal:
                pygame.draw.rect(self.screen, config.RED, c)
            else:
                pygame.draw.rect(self.screen, config.WHITE, c, width=config.CELL_FRAME)

    def possibleActions(self, s):
        """
        Get such actions that don't cause agent go off the grid.
        """
        new_states = self.actions + s
        possible_a = np.where((new_states[:, 0] < self.height) & (new_states[:, 0] >= 0) &
                             (new_states[:, 1] < self.width) & (new_states[:, 1] >= 0))
        return self.actions[possible_a]

    # TODO: refactor this function
    def applyWind(self, sa):
        """
        Apply influence of wind with respect to current state-action.
        """
        a_wind = np.copy(self.actions[sa[-1]])
        w = self.wind[sa[1]]
        a_wind[0] += w
        a_wind[0] = a_wind[0] if a_wind[0] + sa[0] >= 0 else 0
        return a_wind

    def finish(self, s):
        """
        Check if agent reached terminal state.
        """
        return s == self.terminal
