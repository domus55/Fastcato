import pygame

import CloudManager
import Deadline
import FinishPoint
import GameInfo
import MainMenu
import Player
import Block
from Obstacles import ObstacleManager


class LevelManager:
    IMG_LEVELS = []

    #SPECIAL COLORS
    PLAYER_SPAWN = (255, 0, 0, 255)
    FINISH_LINE = (200, 200, 0, 255)

    #BLOCKS
    GRASS = (80, 40, 40, 255)

    #ENITIES
    HEADGEHOG = (200, 100, 100, 255)

    currentLevel = 1
    currentLevelImg = pygame.image.load("images/levels/1.bmp")
    player = None

    @staticmethod
    def Initialize():
        LevelManager.currentLevel = 0
        LevelManager._loadImages()
        LevelManager.restartLevel()

    @staticmethod
    def restartLevel():
        Player.Player.getInstance().restart()
        Block.Block.allBlocks.clear()
        ObstacleManager.ObstacleManager.allObstacles.clear()
        LevelManager.currentLevelImg = LevelManager.IMG_LEVELS[LevelManager.currentLevel]

        if LevelManager.currentLevel == 0:
            Player.Player._instance = None
            MainMenu.MainMenu.open()
        else:
            LevelManager.loadLevel()

    @staticmethod
    def nextLevel():
        LevelManager.currentLevel += 1
        LevelManager.restartLevel()

    @staticmethod
    def loadLevel():
        for i in range(100):
            for j in range(20):
                if LevelManager.currentLevelImg.get_at((i, j)) == LevelManager.GRASS:
                    Block.Block.createBlock(Block.BlockType.GRASS, (i, j))
                if LevelManager.currentLevelImg.get_at((i, j)) == LevelManager.PLAYER_SPAWN:
                    Player.Player.getInstance().startingPosition = (i * 50, j * 50)
                if LevelManager.currentLevelImg.get_at((i, j)) == LevelManager.HEADGEHOG:
                    ObstacleManager.ObstacleManager.createObstacle(ObstacleManager.ObstacleType.HEADGEHOG, (i, j))
                if LevelManager.currentLevelImg.get_at((i, j)) == LevelManager.FINISH_LINE:
                    FinishPoint.FinishPoint.instance = FinishPoint.FinishPoint((i, j))

        ObstacleManager.ObstacleManager.createObstacle(ObstacleManager.ObstacleType.HEADGEHOG, (2, 16))
        ObstacleManager.ObstacleManager.createObstacle(ObstacleManager.ObstacleType.DOG, (7, 16))

        Block.Block.setBlocks()
        Player.Player.getInstance().restart()

    @staticmethod
    def _loadImages():
        try:
            LevelManager.IMG_LEVELS.append(None)
            for i in range(GameInfo.GameInfo.NUMBER_OF_LEVELS):
                #print(f"images/levels/{i+1}.bmp")
                img = pygame.image.load(f"images/levels/{i+1}.bmp")
                LevelManager.IMG_LEVELS.append(img)
        except:
            print("Not all levels *.bmp files are existing!")


