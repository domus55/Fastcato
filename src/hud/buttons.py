import pygame

from src import in_game_menu
from src.project_common import loadImage, PATH
from src.screen import screen


class Buttons:
    BUTTON_SCALE = 4
    BUTTON_SIZE = (50 * BUTTON_SCALE, 55 * BUTTON_SCALE)
    PAUSE_SIZE = (30 * BUTTON_SCALE, 33 * BUTTON_SCALE)

    # Images
    JUMP_UP = loadImage(f"{PATH}images/gui/buttons/jumpUp.png", BUTTON_SIZE)
    JUMP_DOWN = loadImage(f"{PATH}images/gui/buttons/jumpDown.png", BUTTON_SIZE)
    DASH_UP = loadImage(f"{PATH}images/gui/buttons/dashUp.png", BUTTON_SIZE)
    DASH_DOWN = loadImage(f"{PATH}images/gui/buttons/dashDown.png", BUTTON_SIZE)
    PAUSE_UP = loadImage(f"{PATH}images/gui/buttons/pauseUp.png", PAUSE_SIZE)
    PAUSE_DOWN = loadImage(f"{PATH}images/gui/buttons/pauseDown.png", PAUSE_SIZE)

    alpha = 200
    JUMP_UP.set_alpha(alpha)
    JUMP_DOWN.set_alpha(alpha)
    DASH_UP.set_alpha(alpha)
    DASH_DOWN.set_alpha(alpha)

    jumpImg = JUMP_UP
    dashImg = DASH_UP
    pauseImg = PAUSE_UP

    # hitboxes
    hitboxJump = pygame.Rect(0, 750 - BUTTON_SIZE[1] * 2, 100 + BUTTON_SIZE[0], 75 + BUTTON_SIZE[1])
    hitboxDash = pygame.Rect(0, 825 - BUTTON_SIZE[1], 100 + BUTTON_SIZE[0], 75 + BUTTON_SIZE[1])
    hitboxLeft1 = pygame.Rect(100 + BUTTON_SIZE[0], 0, 1100 - BUTTON_SIZE[0], 900)
    hitboxLeft2 = pygame.Rect(0, 0, 100 + BUTTON_SIZE[0], 750 - BUTTON_SIZE[1] * 2)
    hitboxRight = pygame.Rect(1200, 0, 800, 900)
    hitboxPause = pygame.Rect(1500 - PAUSE_SIZE[0], 0, PAUSE_SIZE[0] + 100, PAUSE_SIZE[1] + 100)

    right = False
    left = False
    jump = False
    dash = False

    @staticmethod
    def update(fingers):
        Buttons.jumpImg = Buttons.JUMP_UP
        Buttons.dashImg = Buttons.DASH_UP

        Buttons.right = False
        Buttons.left = False
        Buttons.jump = False
        Buttons.dash = False
        pause = False

        for finger, pos in fingers.items():
            if Buttons.hitboxJump.collidepoint(pos):
                Buttons.jumpImg = Buttons.JUMP_DOWN
                Buttons.jump = True

            if Buttons.hitboxDash.collidepoint(pos):
                Buttons.dashImg = Buttons.DASH_DOWN
                Buttons.dash = True

            if Buttons.hitboxRight.collidepoint(pos):
                Buttons.right = True

            if Buttons.hitboxLeft1.collidepoint(pos) or Buttons.hitboxLeft2.collidepoint(pos):
                Buttons.left = True

            if Buttons.hitboxPause.collidepoint(pos):
                Buttons.pauseImg = Buttons.PAUSE_DOWN
                pause = True
                Buttons.right = False

        if pause is False and Buttons.pauseImg == Buttons.PAUSE_DOWN and in_game_menu.InGameMenu.state is in_game_menu.InGameMenu.State.CLOSED:
            Buttons.pauseImg = Buttons.PAUSE_UP
            in_game_menu.InGameMenu.open()

    @staticmethod
    def render():
        #pygame.draw.rect(screen, (0, 255, 0), Buttons.hitboxLeft1)
        #pygame.draw.rect(screen, (155, 255, 150), Buttons.hitboxLeft2)
        #pygame.draw.rect(screen, (255, 0, 0), Buttons.hitboxRight)
        #pygame.draw.rect(screen, (0, 0, 255), Buttons.hitboxPause)
        #pygame.draw.rect(screen, (255, 0, 0), Buttons.hitboxJump)
        #pygame.draw.rect(screen, (140, 0, 140), Buttons.hitboxDash)

        screen.blit(Buttons.jumpImg, (50, 800 - Buttons.BUTTON_SIZE[1] * 2))
        screen.blit(Buttons.dashImg, (50, 850 - Buttons.BUTTON_SIZE[1]))
        screen.blit(Buttons.pauseImg, (1550 - Buttons.BUTTON_SCALE * 30, 50))


