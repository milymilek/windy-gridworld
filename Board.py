import random
import pygame

import utils
from Cell import Cell


class Board:
    def __init__(self, screen, n):
        self.screen = screen
        self.track = {"track": [], "start": [], "meta": [], "wall": []}
        self.colors = {"track": utils.RED, "start": utils.GREEN, "meta": utils.YELLOW, "wall": utils.WHITE}
        self.n = n

    def createGrid(self):
        for x in range(0, self.n):
            for y in range(0, self.n):
                self.track["wall"].append(Cell(self, x, y, False))

    def draw(self):
        for k in self.track:
            for c in self.track[k]:
                pygame.draw.rect(self.screen, self.colors[k], c, width=1)

    def setTrack(self, cell, track_type):
        cell.track = not cell.track
        if cell.track:
            self.track["wall"].remove(cell)
            self.track[track_type].append(cell)
        else:
            self.track["wall"].append(cell)
            self.track[track_type].remove(cell)

    def loadTrack(self, loaded_track):
        self.track = loaded_track
        print(self.track["track"][0].track)

    def clearBoard(self):
        self.track = {"track": [], "start": [], "meta": [], "wall": []}

    def getRandomStart(self):
        cell = random.choice(self.track["start"])
        return cell.xx, cell.yy
