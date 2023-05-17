import pygame

import FinishPoint
import Player
import Block
from Obstacles import ObstacleManager


class LevelManager:
    LEVEL1 = pygame.image.load("images/levels/1.bmp")
    LEVEL2 = pygame.image.load("images/levels/2.bmp")

    #SPECIAL
    PLAYER_SPAWN = (255, 0, 0, 255)
    FINISH_LINE = (200, 200, 0, 255)

    #BLOCKS
    GRASS = (80, 40, 40, 255)

    #ENITIES
    HEADGEHOG = (200, 100, 100, 255)

    currentLevel = 1
    currentLevelImg = LEVEL1
    player = None

    @staticmethod
    def Initialize():
        LevelManager.currentLevel = 1
        LevelManager.restartLevel()

    @staticmethod
    def update():
        pass

    @staticmethod
    def restartLevel():
        Player.Player.instance.restart()
        Block.Block.allBlocks.clear()
        ObstacleManager.ObstacleManager.allObstacles.clear()

        if LevelManager.currentLevel == 1:
            LevelManager.currentLevelImg = LevelManager.LEVEL1
        elif LevelManager.currentLevel == 2:
            LevelManager.currentLevelImg = LevelManager.LEVEL2

        LevelManager.level1()

    @staticmethod
    def nextLevel():
        LevelManager.currentLevel += 1
        FinishPoint.FinishPoint.instance = None
        LevelManager.restartLevel()

    @staticmethod
    def level1():
        for i in range(100):
            for j in range(20):
                if LevelManager.currentLevelImg.get_at((i, j)) == LevelManager.GRASS:
                    Block.Block.createBlock(Block.BlockType.GRASS, (i, j))
                if LevelManager.currentLevelImg.get_at((i, j)) == LevelManager.PLAYER_SPAWN:
                    Player.Player.instance.startingPosition = (i * 50, j * 50)
                if LevelManager.currentLevelImg.get_at((i, j)) == LevelManager.HEADGEHOG:
                    ObstacleManager.ObstacleManager.createObstacle(ObstacleManager.ObstacleType.HEADGEHOG, (i, j))
                if LevelManager.currentLevelImg.get_at((i, j)) == LevelManager.FINISH_LINE:
                    FinishPoint.FinishPoint.instance = FinishPoint.FinishPoint((i, j))

        ObstacleManager.ObstacleManager.createObstacle(ObstacleManager.ObstacleType.HEADGEHOG, (2, 16))

        Block.Block.setBlocks()
        Player.Player.instance.restart()



