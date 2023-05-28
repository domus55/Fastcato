import pygame

import Camera
import Deadline
import GameInfo
import LevelManager
import Player
from Screen import screen


class FinishPoint(pygame.sprite.Sprite):
    instance = None
    IMG_BIRD = pygame.image.load("images/bird2/1.png").convert()

    def __init__(self, pos):
        super().__init__()
        SIZE = 25
        self.image = pygame.transform.scale(FinishPoint.IMG_BIRD, (SIZE * 1.4, SIZE * 1.3))
        self.rect = self.image.get_rect()
        self.rect.center = pos[0] * 50, pos[1] * 50 + 8

    @staticmethod
    def render():
        if FinishPoint.instance is not None:
            screen.blit(FinishPoint.instance.image, Camera.Camera.relativePosition(FinishPoint.instance.rect.topleft))

    @staticmethod
    def update():
        if FinishPoint.instance is not None:
            if FinishPoint.instance.rect.colliderect(Player.Player.getInstance().collider):
                if GameInfo.GameInfo.levelTime[LevelManager.LevelManager.currentLevel] == 0.0 or\
                        GameInfo.GameInfo.levelTime[LevelManager.LevelManager.currentLevel] > Deadline.Deadline.time():
                    GameInfo.GameInfo.levelTime[LevelManager.LevelManager.currentLevel] = Deadline.Deadline.time()
                    GameInfo.GameInfo.saveSave()
                if Deadline.Deadline.time() <= 60:
                    LevelManager.LevelManager.nextLevel()
                else:
                    LevelManager.LevelManager.restartLevel()
