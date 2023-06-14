import pygame

screen = pygame.display.set_mode((1600, 900))


def screenInitialize():
    pygame.display.set_caption('Cat Game')
    icon = pygame.image.load(f"images/gameIcon.png")
    pygame.display.set_icon(icon)


def screenRender():
    pygame.display.update()
