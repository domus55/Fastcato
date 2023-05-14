import Player
import Block


class LevelManager:
    def __init__(self):
        self.currentLevel = 1
        self.player = Player.Player()
        self.level1()

    def update(self):
        pass

    def level1(self):
        for i in range(20):
            Block.Block.createBlock(Block.BlockType.GRASS, (i + 1, 10))
            Block.Block.createBlock(Block.BlockType.GRASS, (i + 1, 11))
            Block.Block.createBlock(Block.BlockType.GRASS, (i + 1, 12))

        for i in range(4):
            Block.Block.createBlock(Block.BlockType.GRASS, (i + 7, 6))

        Block.Block.createBlock(Block.BlockType.GRASS, (12, 6))

        Block.Block.setBlocks()



