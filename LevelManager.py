import pygame

import Icons
import Camera
import Bird
import Decorations
import GameInfo
import MainMenu
import Player
import Block
import Result
from HUD import BirdCounter, Deadline
from Obstacles import ObstacleManager
from Obstacles.Dog import Dog
from Obstacles.Hedgehog import Hedgehog


class LevelManager:
    IMG_LEVELS = []

    #SPECIAL COLORS
    PLAYER_SPAWN = (255, 0, 0, 255)
    FINISH_LINE = (200, 200, 0, 255)

    #BLOCKS
    BLOCK_GRASS = (80, 40, 40, 255)
    BLOCK_GRASS_BACKGROUND = (50, 25, 25, 255)

    #DECORATIONS
    TREE_BIG = (0, 80, 0, 255)
    TREE_SMALL = (0, 140, 0, 255)
    GRASS = (0, 255, 0, 255)
    BUSH = (100, 200, 100, 255)
    STONE_BIG = (150, 150, 150, 255)
    STONE_SMALL = (200, 200, 200, 255)

    #ENITIES
    HEADGEHOG = (200, 100, 100, 255)
    DOG = (200, 120)

    #Icons
    DEATH = (180, 200, 180)
    ATTENTION = (180, 215, 180)
    STAR = (180, 230, 180)

    currentLevel = 1
    currentLevelImg = pygame.image.load("images/levels/1.bmp")

    @staticmethod
    def initialize():
        LevelManager.currentLevel = 0
        LevelManager._loadImages()
        LevelManager.restartLevel()

    @staticmethod
    def update():
        #print("update")
        if Bird.Bird.birdsOnMap() is 0:
            newRecord = False
            if GameInfo.GameInfo.levelTime[LevelManager.currentLevel] > Deadline.Deadline.time():
                newRecord = True

            #if new record, then save it
            if GameInfo.GameInfo.levelTime[LevelManager.currentLevel] == 0.0 or \
                    newRecord:
                GameInfo.GameInfo.levelTime[LevelManager.currentLevel] = Deadline.Deadline.time()
                GameInfo.GameInfo.saveSave()

            if Result.Result.state == Result.Result.State.closed:
                tooSlow = False if Deadline.Deadline.time() < 60 else True
                Result.Result.open(Deadline.Deadline.strTime(), newRecord, tooSlow)


    @staticmethod
    def restartLevel():
        #Player.Player.getInstance().restart()
        Block.Block.allBlocks.clear()
        Block.Block.allColliders.clear()
        Block.Block.allBackgroundBlocks.clear()
        ObstacleManager.ObstacleManager.allObstacles.clear()
        Bird.Bird.allBirds.clear()
        Icons.Icons.allButton.clear()
        Decorations.Decorations.allDecorations.clear()

        try:
            LevelManager.currentLevelImg = LevelManager.IMG_LEVELS[LevelManager.currentLevel]
        except:
            LevelManager.currentLevelImg = LevelManager.IMG_LEVELS[1]
            LevelManager.currentLevel = 1

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
        for i in range(LevelManager.currentLevelImg.get_width()):
            for j in range(20):
                if LevelManager.currentLevelImg.get_at((i, j)) == LevelManager.BLOCK_GRASS:
                    Block.Block.createBlock(Block.BlockType.GRASS, (i, j))
                if LevelManager.currentLevelImg.get_at((i, j)) == LevelManager.BLOCK_GRASS_BACKGROUND:
                    Block.Block.createBlock(Block.BlockType.GRASS_BACKGROUND, (i, j))
                if LevelManager.currentLevelImg.get_at((i, j)) == LevelManager.PLAYER_SPAWN:
                    Player.Player.getInstance().startingPosition = (i * 50, j * 50)
                #Obstacles
                if LevelManager.currentLevelImg.get_at((i, j)) == LevelManager.HEADGEHOG:
                    obj = Hedgehog((i, j))
                    ObstacleManager.ObstacleManager.addObstacle(obj)
                if LevelManager.currentLevelImg.get_at((i, j))[:2] == LevelManager.DOG:
                    distance = LevelManager.currentLevelImg.get_at((i, j))[2] - 100
                    distance *= 50
                    obj = Dog((i, j), distance)
                    ObstacleManager.ObstacleManager.addObstacle(obj)
                if LevelManager.currentLevelImg.get_at((i, j)) == LevelManager.FINISH_LINE:
                    Bird.Bird.create((i, j))
                #Decorations
                if LevelManager.currentLevelImg.get_at((i, j)) == LevelManager.TREE_BIG:
                    Decorations.Decorations.add(Decorations.Decorations.Type.TREE_BIG, (i, j))
                if LevelManager.currentLevelImg.get_at((i, j)) == LevelManager.TREE_SMALL:
                    Decorations.Decorations.add(Decorations.Decorations.Type.TREE_SMALL, (i, j))
                if LevelManager.currentLevelImg.get_at((i, j)) == LevelManager.GRASS:
                    Decorations.Decorations.add(Decorations.Decorations.Type.GRASS, (i, j))
                if LevelManager.currentLevelImg.get_at((i, j)) == LevelManager.BUSH:
                    Decorations.Decorations.add(Decorations.Decorations.Type.BUSH, (i, j))
                if LevelManager.currentLevelImg.get_at((i, j)) == LevelManager.STONE_BIG:
                    Decorations.Decorations.add(Decorations.Decorations.Type.STONE_BIG, (i, j))
                if LevelManager.currentLevelImg.get_at((i, j)) == LevelManager.STONE_SMALL:
                    Decorations.Decorations.add(Decorations.Decorations.Type.STONE_SMALL, (i, j))
                #Icons
                if LevelManager.currentLevelImg.get_at((i, j)) == LevelManager.DEATH:
                    Icons.Icons.add(Icons.Icons.Type.DEATH, (i * 50 - 22, j * 50))
                if LevelManager.currentLevelImg.get_at((i, j)) == LevelManager.ATTENTION:
                    Icons.Icons.add(Icons.Icons.Type.ATTENTION, (i * 50 - 22, j * 50))
                if LevelManager.currentLevelImg.get_at((i, j)) == LevelManager.STAR:
                    Icons.Icons.add(Icons.Icons.Type.STAR, (i * 50 - 22, j * 50))

        LevelManager._loadAdditionalThings()

        Camera.Camera.borderRight = LevelManager.currentLevelImg.get_width() * 50 - 100
        Player.Player.getInstance().restart()
        BirdCounter.BirdCounter.restart()
        Block.Block.setBlocks()


    @staticmethod
    def _loadImages():
        try:
            LevelManager.IMG_LEVELS.append(None)
            for i in range(GameInfo.GameInfo.NUMBER_OF_LEVELS):
                img = pygame.image.load(f"images/levels/{i+1}.bmp")
                LevelManager.IMG_LEVELS.append(img)
        except:
            print("Not all levels *.bmp files are existing!")

    @staticmethod
    def _loadAdditionalThings():
        if LevelManager.currentLevel is 1:
            x = 325
            y = 500
            Icons.Icons.add(Icons.Icons.Type.W, (x, y - 43))
            Icons.Icons.add(Icons.Icons.Type.A, (x - 45, y))
            Icons.Icons.add(Icons.Icons.Type.S, (x, y))
            Icons.Icons.add(Icons.Icons.Type.D, (x + 45, y))

            Icons.Icons.add(Icons.Icons.Type.TIP, (2100, 550))

            Icons.Icons.add(Icons.Icons.Type.ATTENTION, (1105, 800))

            Icons.Icons.add(Icons.Icons.Type.LSHIFT, (3600, 550))
            Icons.Icons.add(Icons.Icons.Type.ATTENTION, (3625, 500))

            Icons.Icons.add(Icons.Icons.Type.DEATH, (6075, 650))

            Decorations.Decorations.add(Decorations.Decorations.Type.TREE_SMALL, (108, 12))


        if LevelManager.currentLevel is 2:
            Decorations.Decorations.add(Decorations.Decorations.Type.STONE_SMALL, (66, 16))
            Decorations.Decorations.add(Decorations.Decorations.Type.STONE_SMALL, (70, 16))
            Decorations.Decorations.add(Decorations.Decorations.Type.STONE_SMALL, (73, 16))
            Decorations.Decorations.add(Decorations.Decorations.Type.STONE_SMALL, (74, 16))
            Decorations.Decorations.add(Decorations.Decorations.Type.STONE_SMALL, (77, 16))

            obj = Dog((76, 16), -700)
            ObstacleManager.ObstacleManager.addObstacle(obj)


        if LevelManager.currentLevel is 3:
            Icons.Icons.add(Icons.Icons.Type.LSHIFT, (1000, 750))

            obj = Hedgehog((24, 16))
            ObstacleManager.ObstacleManager.addObstacle(obj)

        if LevelManager.currentLevel is 5:
            Bird.Bird.create((64, 17))
            Icons.Icons.add(Icons.Icons.Type.STAR, (64 * 50 - 22, 16 * 50))
            obj = Dog((66, 17), 250)
            ObstacleManager.ObstacleManager.addObstacle(obj)
            obj = Hedgehog((73, 16))
            ObstacleManager.ObstacleManager.addObstacle(obj)
            Decorations.Decorations.add(Decorations.Decorations.Type.STONE_BIG, (69, 17))
            Bird.Bird.create((191, 17))
            Icons.Icons.add(Icons.Icons.Type.STAR, (191 * 50 - 22, 16 * 50))
            obj = Hedgehog((222, 15))
            ObstacleManager.ObstacleManager.addObstacle(obj)
            obj = Dog((225, 16), 250)
            ObstacleManager.ObstacleManager.addObstacle(obj)

        if LevelManager.currentLevel is 6:
            obj = Hedgehog((58, 12))
            ObstacleManager.ObstacleManager.addObstacle(obj)


