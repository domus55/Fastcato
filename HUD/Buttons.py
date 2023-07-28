import pygame

import InGameMenu
from ProjectCommon import loadImage, PATH
from Screen import screen


class Buttons:
    BUTTON_SCALE = 2.5
    BUTTON_SIZE = (50 * BUTTON_SCALE, 55 * BUTTON_SCALE)
    PAUSE_SIZE = (30 * BUTTON_SCALE, 33 * BUTTON_SCALE)

    # Images
    JUMP_UP = loadImage(f"{PATH}images/gui/buttons/jumpUp.png", BUTTON_SIZE)
    JUMP_DOWN = loadImage(f"{PATH}images/gui/buttons/jumpDown.png", BUTTON_SIZE)
    DASH_UP = loadImage(f"{PATH}images/gui/buttons/dashUp.png", BUTTON_SIZE)
    DASH_DOWN = loadImage(f"{PATH}images/gui/buttons/dashDown.png", BUTTON_SIZE)
    PAUSE_UP = loadImage(f"{PATH}images/gui/buttons/PauseUp.png", PAUSE_SIZE)
    PAUSE_DOWN = loadImage(f"{PATH}images/gui/buttons/PauseDown.png", PAUSE_SIZE)

    jumpImg = JUMP_UP
    dashImg = DASH_UP
    pauseImg = PAUSE_UP

    # hitboxes
    hitboxJump = pygame.Rect(50, 850 - BUTTON_SCALE * 50, BUTTON_SIZE[0], BUTTON_SIZE[1])
    hitboxDash = pygame.Rect(100 + BUTTON_SCALE * 50, 850 - BUTTON_SCALE * 50, BUTTON_SIZE[0], BUTTON_SIZE[1])
    hitboxRight = pygame.Rect(800, 0, 400, 900)
    hitboxLeft = pygame.Rect(1200, 0, 400, 900)
    hitboxPause = pygame.Rect(1550 - BUTTON_SCALE * 30, 50, PAUSE_SIZE[0], PAUSE_SIZE[1])

    right = False
    left = False
    jump = False
    dash = False


    @staticmethod
    def update():
        mousePos = pygame.mouse.get_pos()
        if Buttons.hitboxJump.collidepoint(mousePos):
            Buttons.jumpImg = Buttons.JUMP_DOWN
            Buttons.jump = True
        else:
            Buttons.jumpImg = Buttons.JUMP_UP
            Buttons.jump = False

        if Buttons.hitboxDash.collidepoint(mousePos):
            Buttons.dashImg = Buttons.DASH_DOWN
            Buttons.dash = True
        else:
            Buttons.dashImg = Buttons.DASH_UP
            Buttons.dash = False

        if Buttons.hitboxPause.collidepoint(mousePos):
            Buttons.pauseImg = Buttons.PAUSE_DOWN
        else:
            if Buttons.pauseImg == Buttons.PAUSE_DOWN and InGameMenu.InGameMenu.state is InGameMenu.InGameMenu.State.CLOSED:
                InGameMenu.InGameMenu.open()
            Buttons.pauseImg = Buttons.PAUSE_UP

        if Buttons.hitboxRight.collidepoint(mousePos):
            Buttons.right = True
        else:
            Buttons.right = False

        if Buttons.hitboxLeft.collidepoint(mousePos):
            Buttons.left = True
        else:
            Buttons.left = False

    @staticmethod
    def render():
        screen.blit(Buttons.jumpImg, (50, 850 - Buttons.BUTTON_SCALE * 50))
        screen.blit(Buttons.dashImg, (100 + Buttons.BUTTON_SCALE * 50, 850 - Buttons.BUTTON_SCALE * 50))
        screen.blit(Buttons.pauseImg, (1550 - Buttons.BUTTON_SCALE * 30, 50))


        #pygame.draw.rect(screen, (255, 0, 0), Buttons.hitboxJump)
        #pygame.draw.rect(screen, (255, 0, 0), Buttons.hitboxDash)
        #pygame.draw.rect(screen, (255, 0, 0), Buttons.hitboxRight)
        #pygame.draw.rect(screen, (0, 255, 0), Buttons.hitboxLeft)
        #pygame.draw.rect(screen, (0, 0, 255), Buttons.hitboxPause)
