import Player
import pygame

import Game
import GameInfo
from HUD import Deadline, Buttons
from Screen import screen


class Tutorial:
    leftPanel = pygame.Surface((1200, 900), pygame.SRCALPHA, 32)
    rightPanel = pygame.Surface((400, 900), pygame.SRCALPHA, 32)

    showRight = True
    showLeft = False

    @staticmethod
    def render():
        # logic part
        if Game.Game.keyPressed is None or GameInfo.GameInfo.BUILD_TYPE is not GameInfo.BuildType.ANDROID or GameInfo.GameInfo.levelTime[1] != 0:
            return

        if Buttons.Buttons.right or Game.Game.keyPressed[pygame.K_d]:
            if Tutorial.showRight:
                Tutorial.showLeft = True
            Tutorial.showRight = False

        if (Buttons.Buttons.left or Game.Game.keyPressed[pygame.K_a]) and not Tutorial.showRight:
            Tutorial.showLeft = False

        # render part
        alpha1 = abs(100 - (Deadline.Deadline.time()) * 25 % 100)
        alpha2 = abs(100 - (Deadline.Deadline.time() + 2) * 25 % 100)
        if Tutorial.showRight or (Player.Player.getInstance().pos[0] < 900 and Deadline.Deadline.time() >= 12):
            if Deadline.Deadline.time() < 4:
                return
            Tutorial._draw_circle_alpha(Tutorial.rightPanel, (1200, 0), (255, 255, 255, alpha1), (200, 450), 5 * abs(100 - alpha1))
            if (Tutorial.showRight and Deadline.Deadline.time() > 6) or (not Tutorial.showRight and Deadline.Deadline.time() >= 14 ):
                Tutorial._draw_circle_alpha(Tutorial.rightPanel, (1200, 0), (255, 255, 255, alpha2), (200, 450), 5 * abs(100 - alpha2))

        if Tutorial.showLeft:
            Tutorial._draw_circle_alpha(Tutorial.leftPanel, (0, 0), (255, 255, 255, alpha1), (600, 450), 8 * abs(100 - alpha1))
            if Deadline.Deadline.time() > 2:
                Tutorial._draw_circle_alpha(Tutorial.leftPanel, (0, 0), (255, 255, 255, alpha2), (600, 450), 8 * abs(100 - alpha2))

    @staticmethod
    def _draw_circle_alpha(panel, panelPos, color, center, radius):
        target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
        shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
        pygame.draw.circle(shape_surf, color, (radius, radius), radius)
        panel.fill((0, 0, 0, 0))
        panel.blit(shape_surf, target_rect)
        screen.blit(panel, panelPos)
