import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib import cm
import pygame
import sys
import utils
from Agent import Agent
from Board import Board
from Cell import Cell
from Button import Button
import random
from Vehicle import Vehicle
import itertools

SCREEN = pygame.display.set_mode((utils.WINDOW_SIZE, utils.WINDOW_SIZE + 100))
CLOCK = pygame.time.Clock()


def set_cell(event, pos):
    clicked_cell = [c for c in itertools.chain.from_iterable(board.track.values()) if c.collidepoint(pos)][0]
    if event.button == 1:
        board.setTrack(clicked_cell, "track")
    elif event.button == 3:
        board.setTrack(clicked_cell, "start")
    elif event.button == 2:
        board.setTrack(clicked_cell, "meta")


def save_action(button, event, pos):
    if event.button == 1 and button.rect.collidepoint(pos):
        print(button.board.track)
        with open("track.txt", "w") as f:
            f.write(str(button.board.track))


def reset_action(button, event, pos):
    if event.button == 1 and button.rect.collidepoint(pos):
        button.board.clearBoard()
        button.board.createGrid()


def load_action(button, event, pos):
    if event.button == 1 and button.rect.collidepoint(pos):
        with open("track_50x50.txt", "r") as f:
            board_track = eval(f.read())
            board.loadTrack(board_track)

def start_action_learn(button, event, pos):
    if event.button == 1 and button.rect.collidepoint(pos):
        episodes = 50000
        agent = Agent(button.board)

        for e in range(1, episodes):
            print(f"Episode: {e}")
            agent.mc_control(CLOCK)
            if not e % 1000:
                print("Evaluation...")
                for ev in range(30):
                    print(f"ev_{ev}:")
                    agent.evaluate(CLOCK)


        print("End of training...")
        agent.save_params()


if __name__ == '__main__':
    pygame.init()

    board = Board(SCREEN, utils.WINDOW_SIZE // utils.BLOCK_SIZE)
    board.createGrid()

    save_img = pygame.image.load('img/save.png')
    save_button = Button(board, 10, utils.WINDOW_SIZE + 10, save_img, save_action)

    reset_img = pygame.image.load('img/reset.png')
    reset_button = Button(board, 80, utils.WINDOW_SIZE + 10, reset_img, reset_action)

    load_img = pygame.image.load('img/load.png')
    load_button = Button(board, 150, utils.WINDOW_SIZE + 10, load_img, load_action)

    start_img = pygame.image.load('img/start.png')
    start_button = Button(board, 220, utils.WINDOW_SIZE + 10, start_img, start_action_learn)

    while True:
        SCREEN.fill(utils.BLACK)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if 0 < pos[0] < utils.WINDOW_SIZE and 0 < pos[1] < utils.WINDOW_SIZE:
                    set_cell(event, pos)
                else:
                    save_button.action(event, pos)
                    reset_button.action(event, pos)
                    load_button.action(event, pos)
                    start_button.action(event, pos)

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        save_button.draw()
        reset_button.draw()
        load_button.draw()
        start_button.draw()
        board.draw()

        pygame.display.update()
