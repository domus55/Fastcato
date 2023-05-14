import Player
import Block
from Obstacles import ObstacleManager


class LevelManager:
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
        LevelManager.player = Player.Player()
        Block.Block.allBlocks.clear()
        ObstacleManager.ObstacleManager.allObstacles.clear()
        LevelManager.level1()

    @staticmethod
    def level1():
        for i in range(20):
            Block.Block.createBlock(Block.BlockType.GRASS, (i + 1, 10))
            Block.Block.createBlock(Block.BlockType.GRASS, (i + 1, 11))
            Block.Block.createBlock(Block.BlockType.GRASS, (i + 1, 12))

        for i in range(4):
            Block.Block.createBlock(Block.BlockType.GRASS, (i + 7, 6))

        Block.Block.createBlock(Block.BlockType.GRASS, (12, 6))

        Block.Block.setBlocks()
        ObstacleManager.ObstacleManager.createObstacle(ObstacleManager.ObstacleType.HEADGEHOG, (12, 5))



