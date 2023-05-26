import pygame

import CloudManager
import Game
import GameInfo
import LevelManager
import Music
import Screen

'''You may find it strange that there are no button graphics. 
It's because instead of creating Button class, it's graphics, event handling
and all of this mess I came with a different approach. I use a default menu image
and whenever user clicks a button - image changes. I use 4 images with clicked buttons
assuming that user will never click more than one button at once. Thanks to that
I can handle all click event in here getting rid of unnecessary mess
'''

class MainMenu:
    isOpen = False
    inSettings = False

    DEFAULT = pygame.transform.scale(pygame.image.load("images/gui/mainMenu/default.png"), (400, 525)).convert_alpha()
    PLAY = pygame.transform.scale(pygame.image.load("images/gui/mainMenu/playActive.png"), (400, 525)).convert_alpha()
    LEVELS = pygame.transform.scale(pygame.image.load("images/gui/mainMenu/levelsActive.png"), (400, 525)).convert_alpha()
    SETTINGS = pygame.transform.scale(pygame.image.load("images/gui/mainMenu/settingActive.png"), (400, 525)).convert_alpha()
    EXIT = pygame.transform.scale(pygame.image.load("images/gui/mainMenu/exitActive.png"), (400, 525)).convert_alpha()

    SETTINGS_DEFAULT = pygame.transform.scale(pygame.image.load("images/gui/mainMenu/settings/default.png"), (400, 525)).convert_alpha()
    SETTINGS_BACK = pygame.transform.scale(pygame.image.load("images/gui/mainMenu/settings/back.png"), (400, 525)).convert_alpha()
    SETTINGS_SOUND_UP = pygame.transform.scale(pygame.image.load("images/gui/mainMenu/settings/soundUp.png"), (400, 525)).convert_alpha()
    SETTINGS_SOUND_DOWN = pygame.transform.scale(pygame.image.load("images/gui/mainMenu/settings/soundDown.png"), (400, 525)).convert_alpha()
    SETTINGS_MUSIC_UP = pygame.transform.scale(pygame.image.load("images/gui/mainMenu/settings/musicUp.png"), (400, 525)).convert_alpha()
    SETTINGS_MUSIC_DOWN = pygame.transform.scale(pygame.image.load("images/gui/mainMenu/settings/musicDown.png"), (400, 525)).convert_alpha()
    SETTINGS_ACTIVE_BAR = pygame.transform.scale(pygame.image.load("images/gui/mainMenu/settings/activeBar.png"), (15, 45)).convert_alpha()

    BACKGROUND1 = pygame.transform.scale(pygame.image.load("images/gui/mainMenu/background/1.png"), (1600, 900)).convert_alpha()
    BACKGROUND2 = pygame.transform.scale(pygame.image.load("images/gui/mainMenu/background/2.png"), (1600, 900)).convert_alpha()

    #Sounds
    pygame.mixer.init()
    CLICK_SOUND = pygame.mixer.Sound("sounds/click.wav")

    hitboxPlay = pygame.Rect(633, 220, 335, 96)
    hitboxLevels = pygame.Rect(633, 341, 335, 96)
    hitboxSettings = pygame.Rect(633, 462, 335, 96)
    hitboxExit = pygame.Rect(633, 583, 335, 96)

    hitboxSettingBack = pygame.Rect(633, 583, 335, 96)

    hitboxSoundUp = pygame.Rect(944, 320, 25, 74)
    hitboxSoundDown = pygame.Rect(918, 320, 25, 74)
    hitboxMusicUp = pygame.Rect(944, 411, 25, 74)
    hitboxMusicDown = pygame.Rect(918, 411, 25, 74)

    image = DEFAULT


    @staticmethod
    def open():
        MainMenu.isOpen = True
        MainMenu.CLICK_SOUND.set_volume(GameInfo.GameInfo.getSound())
        CloudManager.CloudManager.initialize()

    @staticmethod
    def update():
        CloudManager.CloudManager.update()

    @staticmethod
    def render():
        Screen.screen.blit(MainMenu.BACKGROUND1, (-800, 0))
        Screen.screen.blit(MainMenu.BACKGROUND1, (800, 0))
        CloudManager.CloudManager.renderBeforeMountains()
        CloudManager.CloudManager.renderAfterMountains()
        Screen.screen.blit(MainMenu.BACKGROUND2, (0, 0))
        Screen.screen.blit(MainMenu.image, (600, 187))
        if MainMenu.inSettings:
            for i in range(GameInfo.GameInfo._sound):
                Screen.screen.blit(MainMenu.SETTINGS_ACTIVE_BAR, (788 + i * 19, 334))
            for i in range(GameInfo.GameInfo._music):
                Screen.screen.blit(MainMenu.SETTINGS_ACTIVE_BAR, (788 + i * 19, 424))
        #pygame.draw.rect(Screen.screen, (255, 0, 0), MainMenu.hitboxSoundUp)

    @staticmethod
    def mouseButtonDown():
        if MainMenu.isOpen:
            mousePos = pygame.mouse.get_pos()

            if MainMenu.inSettings:
                if MainMenu.hitboxSettingBack.collidepoint(mousePos):
                    MainMenu.image = MainMenu.SETTINGS_BACK
                    MainMenu.CLICK_SOUND.play()
                elif MainMenu.hitboxSoundUp.collidepoint(mousePos):
                    MainMenu.image = MainMenu.SETTINGS_SOUND_UP
                    MainMenu.CLICK_SOUND.play()
                elif MainMenu.hitboxSoundDown.collidepoint(mousePos):
                    MainMenu.image = MainMenu.SETTINGS_SOUND_DOWN
                    MainMenu.CLICK_SOUND.play()
                elif MainMenu.hitboxMusicUp.collidepoint(mousePos):
                    MainMenu.image = MainMenu.SETTINGS_MUSIC_UP
                    MainMenu.CLICK_SOUND.play()
                elif MainMenu.hitboxMusicDown.collidepoint(mousePos):
                    MainMenu.image = MainMenu.SETTINGS_MUSIC_DOWN
                    MainMenu.CLICK_SOUND.play()
            else:
                if MainMenu.hitboxPlay.collidepoint(mousePos):
                    MainMenu.image = MainMenu.PLAY
                    MainMenu.CLICK_SOUND.play()
                elif MainMenu.hitboxLevels.collidepoint(mousePos):
                    MainMenu.image = MainMenu.LEVELS
                    MainMenu.CLICK_SOUND.play()
                elif MainMenu.hitboxSettings.collidepoint(mousePos):
                    MainMenu.image = MainMenu.SETTINGS
                    MainMenu.CLICK_SOUND.play()
                elif MainMenu.hitboxExit.collidepoint(mousePos):
                    MainMenu.image = MainMenu.EXIT
                    MainMenu.CLICK_SOUND.play()

    @staticmethod
    def mouseButtonUp():
        if MainMenu.isOpen:
            mousePos = pygame.mouse.get_pos()

            if MainMenu.inSettings:
                if MainMenu.hitboxSettingBack.collidepoint(mousePos) and MainMenu.image == MainMenu.SETTINGS_BACK:
                    MainMenu.inSettings = False
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
                MainMenu.CLICK_SOUND.set_volume(GameInfo.GameInfo.getSound())
                Music.Music.adjustVolume()
                GameInfo.GameInfo.save()
            else:
                if MainMenu.hitboxPlay.collidepoint(mousePos) and MainMenu.image == MainMenu.PLAY:
                    LevelManager.LevelManager.nextLevel()
                    MainMenu.isOpen = False
                elif MainMenu.hitboxLevels.collidepoint(mousePos) and MainMenu.image == MainMenu.LEVELS:
                    print("Open levels")
                elif MainMenu.hitboxSettings.collidepoint(mousePos) and MainMenu.image == MainMenu.SETTINGS:
                    MainMenu.inSettings = True
                    MainMenu.image = MainMenu.SETTINGS_DEFAULT
                    return
                elif MainMenu.hitboxExit.collidepoint(mousePos) and MainMenu.image == MainMenu.EXIT:
                    Game.Game.isRunning = False

                MainMenu.image = MainMenu.DEFAULT





