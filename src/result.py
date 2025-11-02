from enum import Enum
import pygame

from src import main_menu, screen, level_manager, in_game_menu, game_info
from src.project_common import loadImage, PATH


class Result:
    class State(Enum):
        CLOSED = 0
        OPEN = 1

    state = State.CLOSED
    SCALE = game_info.GameInfo.HUD_SCALE

    DEFAULT = loadImage(f"{PATH}images/gui/result/default.png", (400 * SCALE, 495 * SCALE))
    NEXT = loadImage(f"{PATH}images/gui/result/next.png", (400 * SCALE, 495 * SCALE))
    RESTART = loadImage(f"{PATH}images/gui/result/restart.png", (400 * SCALE, 495 * SCALE))
    HOME = loadImage(f"{PATH}images/gui/result/home.png", (400 * SCALE, 495 * SCALE))

    TROPHY_SIZE = (120 * SCALE, 60 * SCALE)
    TROPHY_NONE = loadImage(f"{PATH}images/gui/trophy/none.png", TROPHY_SIZE)
    TROPHY_BRONZE = loadImage(f"{PATH}images/gui/trophy/bronze.png", TROPHY_SIZE)
    TROPHY_SILVER = loadImage(f"{PATH}images/gui/trophy/silver.png", TROPHY_SIZE)
    TROPHY_GOLD = loadImage(f"{PATH}images/gui/trophy/gold.png", TROPHY_SIZE)

    hitboxHome = pygame.Rect(800 - 167 * SCALE, 450 + 130 * SCALE, 80 * SCALE, 80 * SCALE)
    hitboxRestart = pygame.Rect(800 - 39 * SCALE, 450 + 130 * SCALE, 80 * SCALE, 80 * SCALE)
    hitboxNext = pygame.Rect(800 + 89  * SCALE, 450 + 130 * SCALE, 80 * SCALE, 80 * SCALE)

    FONT = pygame.font.Font(f"{PATH}fonts/timer.ttf", int(48 * SCALE))
    FONT_COLOR = (182, 137, 98)
    _timeStr = ""
    _time = 0
    _tooSlow = False
    _isNewRecord = False

    image = DEFAULT

    @staticmethod
    def open(timeStr, time, isNewRecord):
        Result._timeStr = timeStr
        Result._time = time
        Result._tooSlow = True if time > 60 else False
        Result._isNewRecord = isNewRecord
        Result.state = Result.State.OPEN
        in_game_menu.InGameMenu.state = in_game_menu.InGameMenu.State.CLOSED
        main_menu.MainMenu.SOUND_CLICK.set_volume(game_info.GameInfo.getSound())

    @staticmethod
    def render():
        screen.screen.blit(Result.image, (800 - 200 * Result.SCALE, 450 - 248 * Result.SCALE))

        # Trophy
        tropheePos = (800 - Result.TROPHY_SIZE[0] / 2, 450 - 143 * Result.SCALE)
        trophyType = game_info.GameInfo.getTrophee(level_manager.LevelManager.currentLevel, Result._time)
        if trophyType == 0:
            screen.screen.blit(Result.TROPHY_NONE, tropheePos)
        elif trophyType == 1:
            screen.screen.blit(Result.TROPHY_BRONZE, tropheePos)
        elif trophyType == 2:
            screen.screen.blit(Result.TROPHY_SILVER, tropheePos)
        elif trophyType == 3:
            screen.screen.blit(Result.TROPHY_GOLD, tropheePos)

        # Time
        str1 = "Time: " + Result._timeStr
        surface1 = Result.FONT.render(str1, False, Result.FONT_COLOR)
        str1pos = 800 - Result.FONT.size(str1)[0] / 2
        screen.screen.blit(surface1, (str1pos, 450 - 90 * Result.SCALE))


        # Time for new trophy
        if trophyType != 3:
            if trophyType == 0:
                strr = "Bronze: 60.000"
            elif trophyType == 1:
                strr = "Silver: " + str(game_info.GameInfo.TROPHY_TIMES[level_manager.LevelManager.currentLevel][1]) + ".000"
            else:
                strr = "Gold: " + str(game_info.GameInfo.TROPHY_TIMES[level_manager.LevelManager.currentLevel][0]) + ".000"

            sizeX, _ = Result.FONT.size(strr)
            surface = Result.FONT.render(strr, False, Result.FONT_COLOR)
            screen.screen.blit(surface, (800 - sizeX / 2, 450 - 30 * Result.SCALE))

        # Too slow / new record
        str2 = ""
        if Result._tooSlow:
            str2 = "Too slow"
        elif Result._isNewRecord:
            str2 = "New record!"

        surface2 = Result.FONT.render(str2, False, Result.FONT_COLOR)
        str2pos = 800 - Result.FONT.size(str2)[0] / 2
        screen.screen.blit(surface2, (str2pos, 450 + 30 * Result.SCALE))

        #pygame.draw.rect(Screen.screen, (255, 0, 0), Result.hitboxNext)
        #pygame.draw.rect(Screen.screen, (255, 0, 0), Result.hitboxRestart)
        #pygame.draw.rect(Screen.screen, (255, 0, 0), Result.hitboxHome)

    @staticmethod
    def mouseButtonDown():
        if Result.state == Result.State.OPEN:
            mousePos = pygame.mouse.get_pos()

            if Result.hitboxNext.collidepoint(mousePos) and game_info.GameInfo.levelTime[level_manager.LevelManager.currentLevel] < 60:
                Result.image = Result.NEXT
                main_menu.MainMenu.SOUND_CLICK.play()
            elif Result.hitboxRestart.collidepoint(mousePos):
                Result.image = Result.RESTART
                main_menu.MainMenu.SOUND_CLICK.play()
            elif Result.hitboxHome.collidepoint(mousePos):
                Result.image = Result.HOME
                main_menu.MainMenu.SOUND_CLICK.play()

    @staticmethod
    def mouseButtonUp():
        if Result.state == Result.State.OPEN:
            mousePos = pygame.mouse.get_pos()

            if Result.hitboxNext.collidepoint(mousePos) and Result.image == Result.NEXT:
                Result.state = Result.State.CLOSED
                level_manager.LevelManager.nextLevel()
            elif Result.hitboxRestart.collidepoint(mousePos) and Result.image == Result.RESTART:
                level_manager.LevelManager.restartLevel()
                Result.state = Result.State.CLOSED
            elif Result.hitboxHome.collidepoint(mousePos) and Result.image == Result.HOME:
                main_menu.MainMenu.open()
                Result.state = Result.State.CLOSED

            Result.image = Result.DEFAULT



