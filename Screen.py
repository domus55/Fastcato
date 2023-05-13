import pygame
import Game

screen = pygame.display.set_mode((1600, 900))

#Checks if user pressed 'X' button
def screenUpdate():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Game.Game.isRunning = False
        # TODO: remove
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            Game.Game.isRunning = False


def screenRender():
    pygame.display.update()
