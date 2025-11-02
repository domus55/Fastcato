import pygame

from src import screen
from src.camera import Camera


class Obstacle(pygame.sprite.Sprite):
    def render(self):
        if Camera.isOnScreen(self.rect):
            screen.screen.blit(self.image, Camera.relativePosition(self.rect.topleft))

        #pygame.draw.rect(Screen.screen, (255, 0, 0), pygame.Rect(Camera.Camera.relativePosition(self.hitbox.topleft), self.hitbox.size))
