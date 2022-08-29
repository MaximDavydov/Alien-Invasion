import pygame

from pygame.sprite import Sprite


class Shell(Sprite):
    """Initialise a shell bullet #2"""

    def __init__(self, bb_game):
        super().__init__()
        self.screen = bb_game.screen
        self.settings = bb_game.settings
        self.color = bb_game.settings.bullet_color

        #создание и позиционирование пули
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_hight)
        self.rect.midright = bb_game.alien.rect.midright

        #более точное позиционирование через десятичную дробь
        self.x = float(self.rect.x)

    def update(self):
        #движение пули и обновление ее позиции
        self.x += self.settings.bullet_speed
        self.rect.x = self.x

    def draw_shell(self):
        #отрисовка пули
        pygame.draw.rect(self.screen, self.color, self.rect)
