import pygame

from src import game_info
from src.project_common import PATH

screen = pygame.display.set_mode((1600, 900))


def screenInitialize():
    global screen
    if game_info.GameInfo.BUILD_TYPE == game_info.BuildType.ANDROID or game_info.GameInfo.fullScreen:
        screen = pygame.display.set_mode((1600, 900), pygame.SCALED | pygame.FULLSCREEN)
    pygame.display.set_caption('Fastcato')
    icon = pygame.image.load(f"{PATH}images/gameIcon.png")
    pygame.display.set_icon(icon)


def screenRender():
    pygame.display.update()
