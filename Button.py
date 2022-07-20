import pygame.mouse


# from main import cells

class Button():
    def __init__(self, board, x, y, image, function):
        self.board = board
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.function = function

    def draw(self):
        self.board.screen.blit(self.image, (self.rect.x, self.rect.y))

    # TODO: uzyc wrappera
    def action(self, *args):
        self.function(self, *args)
