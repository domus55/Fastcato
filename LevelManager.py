import pygame

import BirdCounter
import Buttons
import Camera
import CloudManager
import Deadline
import Bird
import Decorations
import GameInfo
import MainMenu
import Player
import Block
import Result
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

    #SYMBOLS
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
                Result.Result.open(Deadline.Deadline.strTime(), newRecord)

            #if Deadline.Deadline.time() <= 60:
            #    LevelManager.nextLevel()
            #else:
            #    LevelManager.restartLevel()


    @staticmethod
    def restartLevel():
        #Player.Player.getInstance().restart()
        Block.Block.allBlocks.clear()
        Block.Block.allColliders.clear()
        ObstacleManager.ObstacleManager.allObstacles.clear()
        Bird.Bird.allBirds.clear()
        Buttons.Buttons.allButton.clear()
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
                if LevelManager.currentLevelImg.get_at((i, j)) == LevelManager.PLAYER_SPAWN:
                    Player.Player.getInstance().startingPosition = (i * 50, j * 50)
                if LevelManager.currentLevelImg.get_at((i, j)) == LevelManager.HEADGEHOG:
                    obj = Hedgehog((i, j))
                    ObstacleManager.ObstacleManager.addObstackle(obj)
                if LevelManager.currentLevelImg.get_at((i, j))[:2] == LevelManager.DOG:
                    distance = LevelManager.currentLevelImg.get_at((i, j))[2] - 100
                    distance *= 50
                    obj = Dog((i, j), distance)
                    ObstacleManager.ObstacleManager.addObstackle(obj)
                if LevelManager.currentLevelImg.get_at((i, j)) == LevelManager.FINISH_LINE:
                    Bird.Bird.create((i, j))
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
                #Symbols
                if LevelManager.currentLevelImg.get_at((i, j)) == LevelManager.DEATH:
                    Buttons.Buttons.add(Buttons.Buttons.Type.DEATH, (i * 50 - 22, j * 50))
                if LevelManager.currentLevelImg.get_at((i, j)) == LevelManager.ATTENTION:
                    Buttons.Buttons.add(Buttons.Buttons.Type.ATTENTION, (i * 50 - 22, j * 50))
                if LevelManager.currentLevelImg.get_at((i, j)) == LevelManager.STAR:
                    Buttons.Buttons.add(Buttons.Buttons.Type.STAR, (i * 50 - 22, j * 50))

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
            Buttons.Buttons.add(Buttons.Buttons.Type.W, (x, y - 43))
            Buttons.Buttons.add(Buttons.Buttons.Type.A, (x - 45, y))
            Buttons.Buttons.add(Buttons.Buttons.Type.S, (x, y))
            Buttons.Buttons.add(Buttons.Buttons.Type.D, (x + 45, y))

            Buttons.Buttons.add(Buttons.Buttons.Type.ATTENTION, (1105, 800))

            #Buttons.Buttons.add(Buttons.Buttons.Type.DEATH, (1725, 750))

            Buttons.Buttons.add(Buttons.Buttons.Type.LSHIFT, (3600, 550))
            Buttons.Buttons.add(Buttons.Buttons.Type.ATTENTION, (3625, 500))

            Buttons.Buttons.add(Buttons.Buttons.Type.DEATH, (6075, 650))

            Decorations.Decorations.add(Decorations.Decorations.Type.TREE_SMALL, (108, 12))

        if LevelManager.currentLevel is 3:
            Buttons.Buttons.add(Buttons.Buttons.Type.LSHIFT, (1000, 750))


