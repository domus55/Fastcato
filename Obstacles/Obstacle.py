import pygame

import Camera
import Screen


class Obstacle(pygame.sprite.Sprite):
    def render(self):
        if Camera.Camera.isOnScreen(self.rect):
            Screen.screen.blit(self.image, Camera.Camera.relativePosition(self.rect.topleft))

