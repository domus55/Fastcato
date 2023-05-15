import pygame

import Camera
from Screen import screen


class Headgehog(pygame.sprite.Sprite):
    IMG_HEADGEHOG = pygame.image.load("images/hedgehog/1.png")

    def __init__(self, pos):
        super().__init__()
        SIZE = 25
        self.image = pygame.transform.scale(Headgehog.IMG_HEADGEHOG, (SIZE * 1.4, SIZE))
        self.rect = self.image.get_rect()
        self.rect.center = pos[0] * 50, pos[1] * 50 + 12


    def render(self):
        screen.blit(self.image, Camera.Camera.relativePosition(self.rect.topleft))

    def update(self):
        pass
