import pygame
from enum import Enum

import CloudManager
import Game
import GameInfo
import LevelManager
import Music
import Screen
from ProjectCommon import loadImage, PATH

'''You may find it strange that there are no button graphics. 
It's because instead of creating Button class, it's graphics, event handling
and all of this mess I came with a different approach. I use a default menu image
and whenever user clicks a button - image changes. I use 4 images with clicked buttons
assuming that user will never click more than one button at once. Thanks to that
I can handle all click event in here getting rid of unnecessary mess
'''
class MainMenu:
    class State(Enum):
        CLOSED = 0
        IN_MAIN = 1
        IN_LEVELS = 2
        IN_SETTINGS = 3

    state = State.CLOSED
    levelsPage = 0

    IMG_SIZE = (400, 525)
    DEFAULT = loadImage(f"{PATH}images/gui/mainMenu/default.png", IMG_SIZE)
    PLAY = loadImage(f"{PATH}images/gui/mainMenu/playActive.png", IMG_SIZE)
    LEVELS = loadImage(f"{PATH}images/gui/mainMenu/levelsActive.png", IMG_SIZE)
    SETTINGS = loadImage(f"{PATH}images/gui/mainMenu/settingActive.png", IMG_SIZE)
    EXIT = loadImage(f"{PATH}images/gui/mainMenu/exitActive.png", IMG_SIZE)

    SETTINGS_DEFAULT = loadImage(f"{PATH}images/gui/mainMenu/settings/default.png", IMG_SIZE)
    SETTINGS_BACK = loadImage(f"{PATH}images/gui/mainMenu/settings/back.png", IMG_SIZE)
    SETTINGS_SOUND_UP = loadImage(f"{PATH}images/gui/mainMenu/settings/soundUp.png", IMG_SIZE)
    SETTINGS_SOUND_DOWN = loadImage(f"{PATH}images/gui/mainMenu/settings/soundDown.png", IMG_SIZE)
    SETTINGS_MUSIC_UP = loadImage(f"{PATH}images/gui/mainMenu/settings/musicUp.png", IMG_SIZE)
    SETTINGS_MUSIC_DOWN = loadImage(f"{PATH}images/gui/mainMenu/settings/musicDown.png", IMG_SIZE)
    SETTINGS_ACTIVE_BAR = loadImage(f"{PATH}images/gui/mainMenu/settings/activeBar.png", (15, 45))

    LEVELS_DEFAULT = loadImage(f"{PATH}images/gui/mainMenu/levels/default.png", IMG_SIZE)
    LEVELS_BACK = loadImage(f"{PATH}images/gui/mainMenu/levels/back.png", IMG_SIZE)
    LEVELS_NEXT = loadImage(f"{PATH}images/gui/mainMenu/levels/next.png", IMG_SIZE)
    LEVELS_PREV = loadImage(f"{PATH}images/gui/mainMenu/levels/prev.png", IMG_SIZE)
    LEVELS_1 = loadImage(f"{PATH}images/gui/mainMenu/levels/1.png", IMG_SIZE)
    LEVELS_2 = loadImage(f"{PATH}images/gui/mainMenu/levels/2.png", IMG_SIZE)
    LEVELS_3 = loadImage(f"{PATH}images/gui/mainMenu/levels/3.png", IMG_SIZE)

    BACKGROUND1 = loadImage(f"{PATH}images/gui/mainMenu/background/1.png", (1600, 900))
    BACKGROUND2 = loadImage(f"{PATH}images/gui/mainMenu/background/2.png", (1600, 900))

    pygame.font.init()
    FONT = pygame.font.Font(f"{PATH}fonts/mainMenu.ttf", 28)
    FONT_COLOR = (182, 137, 98)

    #Sounds
    pygame.mixer.init()
    SOUND_CLICK = pygame.mixer.Sound(f"{PATH}sounds/click.wav")

    #main hitboxes
    hitboxPlay = pygame.Rect(633, 220, 335, 96)
    hitboxLevels = pygame.Rect(633, 341, 335, 96)
    hitboxSettings = pygame.Rect(633, 462, 335, 96)
    hitboxExit = pygame.Rect(633, 583, 335, 96)

    #settings hitboxes
    hitboxSettingBack = pygame.Rect(633, 583, 335, 96)
    hitboxSoundUp = pygame.Rect(944, 320, 25, 74)
    hitboxSoundDown = pygame.Rect(918, 320, 25, 74)
    hitboxMusicUp = pygame.Rect(944, 411, 25, 74)
    hitboxMusicDown = pygame.Rect(918, 411, 25, 74)

    #levels hitboxes
    hitboxLevelsBack = pygame.Rect(633, 583, 272, 96)
    hitboxLevelsPrev = pygame.Rect(918, 583, 25, 96)
    hitboxLevelsNext = pygame.Rect(944, 583, 25, 96)
    hitboxLevels1 = pygame.Rect(633, 313, 335, 64)
    hitboxLevels2 = pygame.Rect(633, 404, 335, 64)
    hitboxLevels3 = pygame.Rect(633, 494, 335, 64)

    image = DEFAULT

    @staticmethod
    def open():
        MainMenu.state = MainMenu.State.IN_MAIN
        MainMenu.SOUND_CLICK.set_volume(GameInfo.GameInfo.getSound())
        CloudManager.CloudManager.initialize()
        MainMenu.renderBackground()

    @staticmethod
    def update():
        CloudManager.CloudManager.update()

    @staticmethod
    def render():
        if GameInfo.GameInfo.BUILD_TYPE is not GameInfo.BuildType.WEB:
            MainMenu.renderBackground()
        Screen.screen.blit(MainMenu.image, (600, 187))

        if MainMenu.state is MainMenu.State.IN_SETTINGS:
            for i in range(GameInfo.GameInfo._sound):
                Screen.screen.blit(MainMenu.SETTINGS_ACTIVE_BAR, (788 + i * 19, 334))
            for i in range(GameInfo.GameInfo._music):
                Screen.screen.blit(MainMenu.SETTINGS_ACTIVE_BAR, (788 + i * 19, 424))
        if MainMenu.state is MainMenu.State.IN_LEVELS:
            for i in range(3):
                lvl = MainMenu.levelsPage*3+i+1
                posY = 329 + i * 91

                if eval("MainMenu.LEVELS_" + str(i+1)) is MainMenu.image:
                    posY += 8

                surface1 = MainMenu.FONT.render(str(lvl), False, MainMenu.FONT_COLOR)
                surface2 = MainMenu.FONT.render(GameInfo.GameInfo.strLevelTime(lvl), False, MainMenu.FONT_COLOR)

                Screen.screen.blit(surface1, (650, posY))
                Screen.screen.blit(surface2, (811, posY))

        #pygame.draw.rect(Screen.screen, (255, 0, 0), MainMenu.hitboxLevelsBack)

    @staticmethod
    def renderBackground():
        Screen.screen.blit(MainMenu.BACKGROUND1, (-800, 0))
        Screen.screen.blit(MainMenu.BACKGROUND1, (800, 0))
        CloudManager.CloudManager.renderBeforeMountains()
        CloudManager.CloudManager.renderAfterMountains()
        Screen.screen.blit(MainMenu.BACKGROUND2, (0, 0))

    @staticmethod
    def mouseButtonDown():
        if MainMenu.state is not MainMenu.State.CLOSED:
            mousePos = pygame.mouse.get_pos()

            #in settings
            if MainMenu.state is MainMenu.State.IN_SETTINGS:
                if MainMenu.hitboxSettingBack.collidepoint(mousePos):
                    MainMenu.image = MainMenu.SETTINGS_BACK
                    MainMenu.SOUND_CLICK.play()
                elif MainMenu.hitboxSoundUp.collidepoint(mousePos):
                    MainMenu.image = MainMenu.SETTINGS_SOUND_UP
                    MainMenu.SOUND_CLICK.play()
                elif MainMenu.hitboxSoundDown.collidepoint(mousePos):
                    MainMenu.image = MainMenu.SETTINGS_SOUND_DOWN
                    MainMenu.SOUND_CLICK.play()
                elif MainMenu.hitboxMusicUp.collidepoint(mousePos):
                    MainMenu.image = MainMenu.SETTINGS_MUSIC_UP
                    MainMenu.SOUND_CLICK.play()
                elif MainMenu.hitboxMusicDown.collidepoint(mousePos):
                    MainMenu.image = MainMenu.SETTINGS_MUSIC_DOWN
                    MainMenu.SOUND_CLICK.play()
            #in levels
            elif MainMenu.state is MainMenu.State.IN_LEVELS:
                if MainMenu.hitboxLevelsBack.collidepoint(mousePos):
                    MainMenu.image = MainMenu.LEVELS_BACK
                    MainMenu.SOUND_CLICK.play()
                if MainMenu.hitboxLevelsPrev.collidepoint(mousePos):
                    if MainMenu.levelsPage > 0:
                        MainMenu.image = MainMenu.LEVELS_PREV
                        MainMenu.SOUND_CLICK.play()
                if MainMenu.hitboxLevelsNext.collidepoint(mousePos):
                    if MainMenu.levelsPage < 1:
                        MainMenu.image = MainMenu.LEVELS_NEXT
                        MainMenu.SOUND_CLICK.play()
                if MainMenu.hitboxLevels1.collidepoint(mousePos):
                    if GameInfo.GameInfo.levelTime[MainMenu.levelsPage * 3] != 0.0 and GameInfo.GameInfo.levelTime[MainMenu.levelsPage * 3] <= 60.0:
                        MainMenu.image = MainMenu.LEVELS_1
                        MainMenu.SOUND_CLICK.play()
                if MainMenu.hitboxLevels2.collidepoint(mousePos):
                    if GameInfo.GameInfo.levelTime[MainMenu.levelsPage * 3 + 1] != 0.0 and GameInfo.GameInfo.levelTime[MainMenu.levelsPage * 3 + 1] <= 60.0:
                        MainMenu.image = MainMenu.LEVELS_2
                        MainMenu.SOUND_CLICK.play()
                if MainMenu.hitboxLevels3.collidepoint(mousePos):
                    if GameInfo.GameInfo.levelTime[MainMenu.levelsPage * 3 + 2] != 0.0 and GameInfo.GameInfo.levelTime[MainMenu.levelsPage * 3 + 2] <= 60.0:
                        MainMenu.image = MainMenu.LEVELS_3
                        MainMenu.SOUND_CLICK.play()
            #in main
            else:
                if MainMenu.hitboxPlay.collidepoint(mousePos):
                    MainMenu.image = MainMenu.PLAY
                    MainMenu.SOUND_CLICK.play()
                elif MainMenu.hitboxLevels.collidepoint(mousePos):
                    MainMenu.image = MainMenu.LEVELS
                    MainMenu.SOUND_CLICK.play()
                elif MainMenu.hitboxSettings.collidepoint(mousePos):
                    MainMenu.image = MainMenu.SETTINGS
                    MainMenu.SOUND_CLICK.play()
                elif MainMenu.hitboxExit.collidepoint(mousePos):
                    MainMenu.image = MainMenu.EXIT
                    MainMenu.SOUND_CLICK.play()

    @staticmethod
    def mouseButtonUp():
        if MainMenu.state is not MainMenu.State.CLOSED:
            mousePos = pygame.mouse.get_pos()

            #in settings
            if MainMenu.state is MainMenu.State.IN_SETTINGS:
                if MainMenu.hitboxSettingBack.collidepoint(mousePos) and MainMenu.image == MainMenu.SETTINGS_BACK:
                    MainMenu.state = MainMenu.State.IN_MAIN
                    MainMenu.image = MainMenu.DEFAULT
                    return
                elif MainMenu.hitboxSoundUp.collidepoint(mousePos) and MainMenu.image == MainMenu.SETTINGS_SOUND_UP:
                    GameInfo.GameInfo.soundUp()
                elif MainMenu.hitboxSoundDown.collidepoint(mousePos) and MainMenu.image == MainMenu.SETTINGS_SOUND_DOWN:
                    GameInfo.GameInfo.soundDown()
                elif MainMenu.hitboxMusicUp.collidepoint(mousePos) and MainMenu.image == MainMenu.SETTINGS_MUSIC_UP:
                    GameInfo.GameInfo.musicUp()
                elif MainMenu.hitboxMusicDown.collidepoint(mousePos) and MainMenu.image == MainMenu.SETTINGS_MUSIC_DOWN:
                    GameInfo.GameInfo.musicDown()
                MainMenu.image = MainMenu.SETTINGS_DEFAULT
                MainMenu.SOUND_CLICK.set_volume(GameInfo.GameInfo.getSound())
                Music.Music.adjustVolume()
                GameInfo.GameInfo.saveSettings()
            #in levels
            elif MainMenu.state is MainMenu.State.IN_LEVELS:
                if MainMenu.hitboxLevelsBack.collidepoint(mousePos) and MainMenu.image == MainMenu.LEVELS_BACK:
                    MainMenu.state = MainMenu.State.IN_MAIN
                    MainMenu.image = MainMenu.DEFAULT
                    return
                elif MainMenu.hitboxLevelsPrev.collidepoint(mousePos) and MainMenu.image == MainMenu.LEVELS_PREV:
                    MainMenu.levelsPage -= 1
                elif MainMenu.hitboxLevelsNext.collidepoint(mousePos) and MainMenu.image == MainMenu.LEVELS_NEXT:
                    MainMenu.levelsPage += 1
                elif MainMenu.hitboxLevels1.collidepoint(mousePos) and MainMenu.image == MainMenu.LEVELS_1:
                    MainMenu.state = MainMenu.State.IN_MAIN
                    MainMenu.image = MainMenu.DEFAULT
                    LevelManager.LevelManager.currentLevel = MainMenu.levelsPage * 3 + 1
                    LevelManager.LevelManager.restartLevel()
                    MainMenu.state = MainMenu.State.CLOSED
                    return
                elif MainMenu.hitboxLevels2.collidepoint(mousePos) and MainMenu.image == MainMenu.LEVELS_2:
                    MainMenu.state = MainMenu.State.IN_MAIN
                    MainMenu.image = MainMenu.DEFAULT
                    LevelManager.LevelManager.currentLevel = MainMenu.levelsPage * 3 + 2
                    LevelManager.LevelManager.restartLevel()
                    MainMenu.state = MainMenu.State.CLOSED
                    return
                elif MainMenu.hitboxLevels3.collidepoint(mousePos) and MainMenu.image == MainMenu.LEVELS_3:
                    MainMenu.state = MainMenu.State.IN_MAIN
                    MainMenu.image = MainMenu.DEFAULT
                    LevelManager.LevelManager.currentLevel = MainMenu.levelsPage * 3 + 3
                    LevelManager.LevelManager.restartLevel()
                    MainMenu.state = MainMenu.State.CLOSED
                    return
                MainMenu.image = MainMenu.LEVELS_DEFAULT
            #in main
            else:
                if MainMenu.hitboxPlay.collidepoint(mousePos) and MainMenu.image == MainMenu.PLAY:
                    for i in reversed(range(GameInfo.GameInfo.NUMBER_OF_LEVELS)):
                        if GameInfo.GameInfo.levelTime[i] != 0.0 and GameInfo.GameInfo.levelTime[i] <= 60.0:
                            LevelManager.LevelManager.currentLevel = i + 1
                            LevelManager.LevelManager.restartLevel()
                            MainMenu.state = MainMenu.State.CLOSED
                            MainMenu.image = MainMenu.DEFAULT
                            return
                elif MainMenu.hitboxLevels.collidepoint(mousePos) and MainMenu.image == MainMenu.LEVELS:
                    MainMenu.state = MainMenu.State.IN_LEVELS
                    MainMenu.image = MainMenu.LEVELS_DEFAULT
                    return
                elif MainMenu.hitboxSettings.collidepoint(mousePos) and MainMenu.image == MainMenu.SETTINGS:
                    MainMenu.state = MainMenu.State.IN_SETTINGS
                    MainMenu.image = MainMenu.SETTINGS_DEFAULT
                    return
                elif MainMenu.hitboxExit.collidepoint(mousePos) and MainMenu.image == MainMenu.EXIT:
                    Game.Game.isRunning = False

                MainMenu.image = MainMenu.DEFAULT





