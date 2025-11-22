import pygame

from src import bird, block, cat_small, credits, decorations, game_info, icons, main_menu, player, result
from src.camera import Camera
from src.hud import bird_counter, deadline
from src.obstacles import obstacle_manager
from src.obstacles.dog import Dog
from src.obstacles.hedgehog import Hedgehog
from src.project_common import PATH


class LevelManager:
    IMG_LEVELS = []

    # Special colors
    PLAYER_SPAWN = (255, 0, 0, 255)
    BIRD = (200, 200, 0, 255)
    BIRD_WITH_ICON = (220, 200, 0, 255)

    # Blocks
    BLOCK_GRASS = (80, 40, 40, 255)
    BLOCK_GRASS_BACKGROUND = (50, 25, 25, 255)

    # Decorations
    TREE_BIG = (0, 80, 0, 255)
    TREE_SMALL = (0, 140, 0, 255)
    GRASS = (0, 255, 0, 255)
    BUSH = (100, 200, 100, 255)
    STONE_BIG = (150, 150, 150, 255)
    STONE_SMALL = (200, 200, 200, 255)
    BALLOON = (255, 0, 200, 255)

    # Entities
    HEDGEHOG = (200, 100, 100, 255)
    DOG = (200, 120)

    # Icons
    DEATH = (180, 200, 180)
    ATTENTION = (180, 215, 180)
    STAR = (180, 230, 180)

    current_level = 6
    current_level_img = pygame.image.load(f"{PATH}images/levels/1.bmp")

    @staticmethod
    def initialize():
        LevelManager.current_level = 0
        LevelManager._loadImages()
        LevelManager.restartLevel()

    @staticmethod
    def finished_level():
        if LevelManager.current_level == 7:
            return

        new_record = False
        if game_info.GameInfo.level_time[LevelManager.current_level] > deadline.Deadline.time():
            new_record = True

        # if new record, then save it
        if game_info.GameInfo.level_time[LevelManager.current_level] == 0.0 or \
                new_record:
            game_info.GameInfo.level_time[LevelManager.current_level] = deadline.Deadline.time()
            game_info.GameInfo.save_time()

        if result.Result.state == result.Result.State.CLOSED:
            result.Result.open(deadline.Deadline.strTime(), deadline.Deadline.time(), new_record)

    @staticmethod
    def restartLevel():
        block.Block.allBlocks.clear()
        block.Block.allColliders.clear()
        block.Block.allBackgroundBlocks.clear()
        obstacle_manager.ObstacleManager.allObstacles.clear()
        bird.Bird.all_birds.clear()
        icons.Icons.allButton.clear()
        decorations.Decorations.allDecorations.clear()
        deadline.Deadline.restart()

        try:
            LevelManager.current_level_img = LevelManager.IMG_LEVELS[LevelManager.current_level]
        except (IndexError, TypeError, AttributeError):
            LevelManager.current_level_img = LevelManager.IMG_LEVELS[1]
            LevelManager.current_level = 1

        if LevelManager.current_level == 0:
            player.Player._instance = None
            main_menu.MainMenu.open()
        else:
            LevelManager.loadLevel()

    @staticmethod
    def nextLevel():
        LevelManager.current_level += 1
        LevelManager.restartLevel()

    @staticmethod
    def loadLevel():
        for i in range(LevelManager.current_level_img.get_width()):
            for j in range(20):
                if LevelManager.current_level_img.get_at((i, j)) == LevelManager.BLOCK_GRASS:
                    block.Block.createBlock(block.BlockType.GRASS, (i, j))
                if LevelManager.current_level_img.get_at((i, j)) == LevelManager.BLOCK_GRASS_BACKGROUND:
                    block.Block.createBlock(block.BlockType.GRASS_BACKGROUND, (i, j))
                if LevelManager.current_level_img.get_at((i, j)) == LevelManager.PLAYER_SPAWN:
                    player.Player.getInstance().startingPosition = (i * 50, j * 50)
                #obstacles
                if LevelManager.current_level_img.get_at((i, j)) == LevelManager.HEDGEHOG:
                    obj = Hedgehog((i, j))
                    obstacle_manager.ObstacleManager.addObstacle(obj)
                if LevelManager.current_level_img.get_at((i, j))[:2] == LevelManager.DOG:
                    distance = LevelManager.current_level_img.get_at((i, j))[2] - 100
                    distance *= 50
                    obj = Dog((i, j), distance)
                    obstacle_manager.ObstacleManager.addObstacle(obj)
                if LevelManager.current_level_img.get_at((i, j)) == LevelManager.BIRD:
                    bird.Bird.create((i, j))
                if LevelManager.current_level_img.get_at((i, j)) == LevelManager.BIRD_WITH_ICON:
                    bird.Bird.create((i, j), True)
                #Decorations
                if LevelManager.current_level_img.get_at((i, j)) == LevelManager.TREE_BIG:
                    decorations.Decorations.add(decorations.Decorations.Type.TREE_BIG, (i, j))
                if LevelManager.current_level_img.get_at((i, j)) == LevelManager.TREE_SMALL:
                    decorations.Decorations.add(decorations.Decorations.Type.TREE_SMALL, (i, j))
                if LevelManager.current_level_img.get_at((i, j)) == LevelManager.GRASS:
                    decorations.Decorations.add(decorations.Decorations.Type.GRASS, (i, j))
                if LevelManager.current_level_img.get_at((i, j)) == LevelManager.BUSH:
                    decorations.Decorations.add(decorations.Decorations.Type.BUSH, (i, j))
                if LevelManager.current_level_img.get_at((i, j)) == LevelManager.STONE_BIG:
                    decorations.Decorations.add(decorations.Decorations.Type.STONE_BIG, (i, j))
                if LevelManager.current_level_img.get_at((i, j)) == LevelManager.STONE_SMALL:
                    decorations.Decorations.add(decorations.Decorations.Type.STONE_SMALL, (i, j))
                if LevelManager.current_level_img.get_at((i, j)) == LevelManager.BALLOON:
                    decorations.Decorations.add(decorations.Decorations.Type.BALLOON, (i, j))
                #Icons
                if LevelManager.current_level_img.get_at((i, j)) == LevelManager.DEATH:
                    icons.Icons.add(icons.Icons.Type.DEATH, (i * 50 - 22, j * 50))
                if LevelManager.current_level_img.get_at((i, j)) == LevelManager.ATTENTION:
                    icons.Icons.add(icons.Icons.Type.ATTENTION, (i * 50 - 22, j * 50))
                if LevelManager.current_level_img.get_at((i, j)) == LevelManager.STAR:
                    icons.Icons.add(icons.Icons.Type.STAR, (i * 50 - 22, j * 50))

        Camera.borderRight = LevelManager.current_level_img.get_width() * 50 - 100
        player.Player.getInstance().restart()
        bird_counter.BirdCounter.restart()
        LevelManager._loadAdditionalThings()
        block.Block.setBlocks()

    @staticmethod
    def _loadImages():
        try:
            LevelManager.IMG_LEVELS.append(None)
            for i in range(game_info.GameInfo.NUMBER_OF_LEVELS + 1):
                img = pygame.image.load(f"{PATH}images/levels/{i+1}.bmp")
                LevelManager.IMG_LEVELS.append(img)
        except (IndexError, TypeError, AttributeError):
            print("Not all levels *.bmp files are existing!")

    @staticmethod
    def _loadAdditionalThings():
        if LevelManager.current_level == 1:
            x = 500
            y = 500
            icons.Icons.add(icons.Icons.Type.W, (x, y - 43))
            icons.Icons.add(icons.Icons.Type.A, (x - 45, y))
            icons.Icons.add(icons.Icons.Type.S, (x, y))
            icons.Icons.add(icons.Icons.Type.D, (x + 45, y))

            icons.Icons.add(icons.Icons.Type.TIP, (2300, 550))

            icons.Icons.add(icons.Icons.Type.ATTENTION, (1305, 800))

            icons.Icons.add(icons.Icons.Type.LSHIFT, (3800, 550))
            icons.Icons.add(icons.Icons.Type.ATTENTION, (3825, 500))

            icons.Icons.add(icons.Icons.Type.DEATH, (6275, 650))

            decorations.Decorations.add(decorations.Decorations.Type.TREE_SMALL, (112, 12))

        if LevelManager.current_level == 2:
            decorations.Decorations.add(decorations.Decorations.Type.STONE_SMALL, (66, 16))
            decorations.Decorations.add(decorations.Decorations.Type.STONE_SMALL, (70, 16))
            decorations.Decorations.add(decorations.Decorations.Type.STONE_SMALL, (73, 16))
            decorations.Decorations.add(decorations.Decorations.Type.STONE_SMALL, (74, 16))
            decorations.Decorations.add(decorations.Decorations.Type.STONE_SMALL, (77, 16))

            obj = Dog((76, 16), -700)
            obstacle_manager.ObstacleManager.addObstacle(obj)

        if LevelManager.current_level == 3:
            icons.Icons.add(icons.Icons.Type.LSHIFT, (1000, 750))

            obj = Hedgehog((24, 16))
            obstacle_manager.ObstacleManager.addObstacle(obj)

        if LevelManager.current_level == 5:
            block.Block.createBlock(block.BlockType.GRASS_BACKGROUND, (64, 17))
            obj = Dog((66, 17), 250)
            obstacle_manager.ObstacleManager.addObstacle(obj)
            obj = Hedgehog((73, 16))
            obstacle_manager.ObstacleManager.addObstacle(obj)
            decorations.Decorations.add(decorations.Decorations.Type.STONE_BIG, (69, 17))
            block.Block.createBlock(block.BlockType.GRASS_BACKGROUND, (191, 17))
            obj = Hedgehog((222, 15))
            obstacle_manager.ObstacleManager.addObstacle(obj)
            obj = Dog((225, 16), 250)
            obstacle_manager.ObstacleManager.addObstacle(obj)

        if LevelManager.current_level == 6:
            obj = Hedgehog((58, 12))
            obstacle_manager.ObstacleManager.addObstacle(obj)
            Camera.borderRight -= 300

        if LevelManager.current_level == 7:
            cat_small.CatSmall.getInstance().restart([1350, 675])
            decorations.Decorations.add(decorations.Decorations.Type.CAKE, (17, 15))
            bird.Bird.create((15.47, 15))
            bird.Bird.create((18.52, 15))
            credits.Credits.restart()
