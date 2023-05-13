import pygame
from Screen import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/cat.png")
        self.rect = self.image.get_rect()
        self.rect.center = 100, 100

    def update(self):
        pass

    def render(self):
        #screen.blit(self.image, self.rect)
        pass

