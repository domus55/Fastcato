import pygame

import Player
import Block
from Obstacles import ObstacleManager


class LevelManager:
    LEVEL1 = pygame.image.load("images/levels/1.bmp")
    GRASS = (80, 40, 40, 255)
    PLAYER_SPAWN = (255, 0, 0, 255)
    currentLevel = 1
    player = None

    @staticmethod
    def Initialize():
        LevelManager.player = Player.Player()
        LevelManager.level1()

    @staticmethod
    def update():
        pass

    @staticmethod
    def restartLevel():
        LevelManager.player.restart()
        Block.Block.allBlocks.clear()
        ObstacleManager.ObstacleManager.allObstacles.clear()
        LevelManager.level1()

    @staticmethod
    def level1():
        for i in range(30):
            for j in range(20):

                if LevelManager.LEVEL1.get_at((i, j)) == LevelManager.GRASS:
                    Block.Block.createBlock(Block.BlockType.GRASS, (i, j))
                if LevelManager.LEVEL1.get_at((i, j)) == LevelManager.PLAYER_SPAWN:
                    LevelManager.player.startingPosition = (i * 50, j * 50)

        Block.Block.setBlocks()
        LevelManager.player.restart()

        """
        for i in range(20):
            Block.Block.createBlock(Block.BlockType.GRASS, (i + 1, 10))
            Block.Block.createBlock(Block.BlockType.GRASS, (i + 1, 11))
            Block.Block.createBlock(Block.BlockType.GRASS, (i + 1, 12))

        for i in range(4):
            Block.Block.createBlock(Block.BlockType.GRASS, (i + 7, 6))

        Block.Block.createBlock(Block.BlockType.GRASS, (12, 6))

        Block.Block.setBlocks()
        ObstacleManager.ObstacleManager.createObstacle(ObstacleManager.ObstacleType.HEADGEHOG, (12, 5))"""



