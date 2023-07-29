from enum import Enum
import pygame

import GameInfo
import InGameMenu
import LevelManager
import Screen
import MainMenu
from ProjectCommon import loadImage, PATH


class Result:
    class State(Enum):
        CLOSED = 0
        OPEN = 1

    state = State.CLOSED
    SCALE = GameInfo.GameInfo.HUD_SCALE

    DEFAULT = loadImage(f"{PATH}images/gui/result/default.png", (400 * SCALE, 405 * SCALE))
    NEXT = loadImage(f"{PATH}images/gui/result/next.png", (400 * SCALE, 405 * SCALE))
    RESTART = loadImage(f"{PATH}images/gui/result/restart.png", (400 * SCALE, 405 * SCALE))
    HOME = loadImage(f"{PATH}images/gui/result/home.png", (400 * SCALE, 405 * SCALE))

    hitboxHome = pygame.Rect(800 - 167 * SCALE, 450 + 87 * SCALE, 80 * SCALE, 80 * SCALE)
    hitboxRestart = pygame.Rect(800 - 39 * SCALE, 450 + 87 * SCALE, 80 * SCALE, 80 * SCALE)
    hitboxNext = pygame.Rect(800 + 89  * SCALE, 450 + 87 * SCALE, 80 * SCALE, 80 * SCALE)

    FONT = pygame.font.Font(f"{PATH}fonts/timer.ttf", int(48 * SCALE))
    FONT_COLOR = (182, 137, 98)
    _time = ""
    _tooSlow = False
    _isNewRecord = False

    image = DEFAULT

    @staticmethod
    def open(time, isNewRecord, tooSlow):
        Result._time = time
        Result._tooSlow = tooSlow
        Result._isNewRecord = isNewRecord
        Result.state = Result.State.OPEN
        InGameMenu.InGameMenu.state = InGameMenu.InGameMenu.State.CLOSED
        MainMenu.MainMenu.SOUND_CLICK.set_volume(GameInfo.GameInfo.getSound())

    @staticmethod
    def render():
        Screen.screen.blit(Result.image, (800 - 200 * Result.SCALE, 450 - 203 * Result.SCALE))
        str1 = "Time: " + Result._time
        str2 = ""
        str2pos = 0
        if Result._tooSlow:
            str2 = "Too slow"
            str2pos = 800 - 79 * Result.SCALE
        elif Result._isNewRecord:
            str2 = "New record!"
            str2pos = 800 - 107 * Result.SCALE

        surface1 = Result.FONT.render(str1, False, Result.FONT_COLOR)
        surface2 = Result.FONT.render(str2, False, Result.FONT_COLOR)

        Screen.screen.blit(surface1, (800 - 153 * Result.SCALE, 450 - 70 * Result.SCALE))
        Screen.screen.blit(surface2, (str2pos, 450 - 10 * Result.SCALE))

        #pygame.draw.rect(Screen.screen, (255, 0, 0), Result.hitboxNext)
        #pygame.draw.rect(Screen.screen, (255, 0, 0), Result.hitboxRestart)
        #pygame.draw.rect(Screen.screen, (255, 0, 0), Result.hitboxHome)

    @staticmethod
    def mouseButtonDown():
        if Result.state == Result.State.OPEN:
            mousePos = pygame.mouse.get_pos()

            if Result.hitboxNext.collidepoint(mousePos) and GameInfo.GameInfo.levelTime[LevelManager.LevelManager.currentLevel] < 60:
                Result.image = Result.NEXT
                MainMenu.MainMenu.SOUND_CLICK.play()
            elif Result.hitboxRestart.collidepoint(mousePos):
                Result.image = Result.RESTART
                MainMenu.MainMenu.SOUND_CLICK.play()
            elif Result.hitboxHome.collidepoint(mousePos):
                Result.image = Result.HOME
                MainMenu.MainMenu.SOUND_CLICK.play()

    @staticmethod
    def mouseButtonUp():
        if Result.state == Result.State.OPEN:
            mousePos = pygame.mouse.get_pos()

            if Result.hitboxNext.collidepoint(mousePos) and Result.image == Result.NEXT:
                Result.state = Result.State.CLOSED
                LevelManager.LevelManager.nextLevel()
            elif Result.hitboxRestart.collidepoint(mousePos) and Result.image == Result.RESTART:
                LevelManager.LevelManager.restartLevel()
                Result.state = Result.State.CLOSED
            elif Result.hitboxHome.collidepoint(mousePos) and Result.image == Result.HOME:
                MainMenu.MainMenu.open()
                Result.state = Result.State.CLOSED

            Result.image = Result.DEFAULT



