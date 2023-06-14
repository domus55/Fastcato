from enum import Enum
import pygame
import pygame.freetype

import GameInfo
import InGameMenu
import LevelManager
import Screen
import MainMenu


class Result:
    class State(Enum):
        CLOSED = 0
        OPEN = 1

    state = State.CLOSED

    DEFAULT = pygame.transform.scale(pygame.image.load("images/gui/result/default.png"), (400, 405)).convert_alpha()
    NEXT = pygame.transform.scale(pygame.image.load("images/gui/result/next.png"), (400, 405)).convert_alpha()
    RESTART = pygame.transform.scale(pygame.image.load("images/gui/result/restart.png"), (400, 405)).convert_alpha()
    HOME = pygame.transform.scale(pygame.image.load("images/gui/result/home.png"), (400, 405)).convert_alpha()

    hitboxHome = pygame.Rect(633, 537, 80, 80)
    hitboxRestart = pygame.Rect(761, 537, 80, 80)
    hitboxNext = pygame.Rect(889, 537, 80, 80)



    FONT = pygame.freetype.Font("fonts/timer.ttf", 48)
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
        Screen.screen.blit(Result.image, (600, 247))
        str1 = "Time: " + Result._time
        str2 = ""
        str2pos = 0
        if Result._tooSlow:
            str2 = "Too slow"
            str2pos = 721
        elif Result._isNewRecord:
            str2 = "New record!"
            str2pos = 693

        Result.FONT.render_to(Screen.screen, (647, 400), str1, Result.FONT_COLOR)
        Result.FONT.render_to(Screen.screen, (str2pos, 460), str2, Result.FONT_COLOR)

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



