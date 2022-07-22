import numpy as np
import matplotlib.pyplot as plt
import pygame
import sys
import config
from Agent import Agent
from Environment import Environment
from Button import Button

from TDControl import TDControl

GRID_WIDTH = config.WINDOW_WIDTH * config.BLOCK_SIZE
GRID_HEIGHT = config.WINDOW_HEIGHT * config.BLOCK_SIZE
SCREEN = pygame.display.set_mode((GRID_WIDTH, GRID_HEIGHT+config.BLOCK_SIZE))
CLOCK = pygame.time.Clock()

def save_evaluation_results(steps):
    fig = plt.figure(1)
    plt.title("Average Time steps")
    plt.plot(np.arange(len(steps)), steps)
    plt.xlabel("Episode x 1000")
    plt.ylabel("Mean time steps per 30 eval")
    plt.savefig('policy_evaluation.png')
    plt.close(fig)

def start_action_learn(button, event, pos):
    if event.button == 1 and button.rect.collidepoint(pos):
        episodes = 10001
        agent = Agent(button.board)
        td = TDControl(env, agent)
        steps = []

        for e in range(1, episodes):
            print(f"Episode: {e}")
            td.sarsa(CLOCK)
            if not e % 1000:
                print("Evaluation...")
                steps_mean = 0
                for ev in range(30):
                    print(f"ev_{ev}:")
                    steps_mean += td.evaluate(CLOCK)
                steps_mean /= 30
                steps.append(steps_mean)

        save_evaluation_results(steps)
        td.save_params()
        print("End of training...")

def evaluate_params(button, event, pos):
    if event.button == 1 and button.rect.collidepoint(pos):
        print("SDdsvdscvsdf")
        agent = Agent(button.board)
        td = TDControl(env, agent, Q='train_params/Q.npy', PI='train_params/PI.npy')
        i = 0
        while True:
            print(f"eval: {i}...")
            td.evaluate(CLOCK)



if __name__ == '__main__':
    pygame.init()

    env = Environment(SCREEN, config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
    env.createGrid()

    start_img = pygame.image.load('img/start.png')
    eval_img = pygame.image.load('img/eval.png')
    start_button = Button(env, GRID_WIDTH // 2 - config.ICON_SIZE, GRID_HEIGHT + config.BLOCK_SIZE//2 - config.ICON_SIZE,
                          start_img, start_action_learn)
    eval_button = Button(env, GRID_WIDTH - 2 * config.ICON_SIZE, GRID_HEIGHT + config.BLOCK_SIZE//2 - config.ICON_SIZE,
                          eval_img, evaluate_params)

    while True:
        SCREEN.fill(config.BLACK)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                start_button.action(event, pos)
                eval_button.action(event, pos)

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        start_button.draw()
        eval_button.draw()
        env.draw()
        pygame.display.update()
