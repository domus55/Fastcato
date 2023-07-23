import GameInfo
import pygame
from ProjectCommon import PATH

if GameInfo.GameInfo.BUILD_TYPE == GameInfo.BuildType.ANDROID:
    screen = pygame.display.set_mode((1600, 900), pygame.SCALED|pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((1600,900))


def screenInitialize():
    pygame.display.set_caption('FastCato')
    icon = pygame.image.load(f"{PATH}images/gameIcon.png")
    pygame.display.set_icon(icon)


def screenRender():
    pygame.display.update()
