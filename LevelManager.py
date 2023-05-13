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
        b = Block.Block((300, 300))
        Block.Block.allBlocks.append(b)

