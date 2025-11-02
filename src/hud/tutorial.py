import pygame

from src import game_info, player
from src.hud import deadline, buttons
from src.screen import screen


class Tutorial:
    rightPanel = pygame.Surface((400, 900), pygame.SRCALPHA, 32)

    showHint = True

    @staticmethod
    def render(key_pressed):
        # logic part
        if key_pressed is None or game_info.GameInfo.BUILD_TYPE is not game_info.BuildType.ANDROID or game_info.GameInfo.levelTime[1] != 0:
            return

        if buttons.Buttons.right or key_pressed[pygame.K_d]:
            Tutorial.showHint = False

        # render part
        alpha1 = abs(100 - (deadline.Deadline.time()) * 25 % 100)
        alpha2 = abs(100 - (deadline.Deadline.time() + 2) * 25 % 100)
        if Tutorial.showHint or (player.Player.getInstance().pos[0] < 900 and deadline.Deadline.time() >= 8):
            if deadline.Deadline.time() < 4:
                return
            Tutorial._draw_circle_alpha(Tutorial.rightPanel, (1200, 0), (255, 255, 255, alpha1), (200, 450), 5 * abs(100 - alpha1))
            if (Tutorial.showHint and deadline.Deadline.time() > 6) or (not Tutorial.showHint and deadline.Deadline.time() >= 10):
                Tutorial._draw_circle_alpha(Tutorial.rightPanel, (1200, 0), (255, 255, 255, alpha2), (200, 450), 5 * abs(100 - alpha2))

    @staticmethod
    def _draw_circle_alpha(panel, panelPos, color, center, radius):
        target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
        shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
        pygame.draw.circle(shape_surf, color, (radius, radius), radius)
        panel.fill((0, 0, 0, 0))
        panel.blit(shape_surf, target_rect)
        screen.blit(panel, panelPos)
