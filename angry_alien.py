import pygame


class Alien:
    """Class for alien control."""

    def __init__(self, bb_game):
        """Initialize the bird and set its starting position."""
        self.screen = bb_game.screen
        self.settings = bb_game.settings
        self.screen_rect = bb_game.screen.get_rect()

        # Load the alien image and get it rec
        self.image = pygame.image.load('images/angry_alien.bmp')
        self.rect = self.image.get_rect()

        # Start each new bird at the center of the screen.
        self.rect.midleft = self.screen_rect.midleft

        # переводим позицию к флоат
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Тип флага
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        # Обновление позиции пришельца основанное на позиции флага
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        elif self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        elif self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        # обновляем значение прямоугольника
        self.rect.x, self.rect.y = self.x, self.y

    def blitme(self):
        """Draw alien in current position."""
        self.screen.blit(self.image, self.rect)
