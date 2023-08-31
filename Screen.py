import GameInfo
import pygame
from ProjectCommon import PATH

screen = pygame.display.set_mode((1600, 900))


def screenInitialize():
    global screen
    if GameInfo.GameInfo.BUILD_TYPE == GameInfo.BuildType.ANDROID or GameInfo.GameInfo.fullScreen:
        screen = pygame.display.set_mode((1600, 900), pygame.SCALED | pygame.FULLSCREEN)
    pygame.display.set_caption('Fastcato')
    icon = pygame.image.load(f"{PATH}images/gameIcon.png")
    pygame.display.set_icon(icon)


def screenRender():
    pygame.display.update()
