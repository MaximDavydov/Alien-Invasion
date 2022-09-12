import pygame
from pygame.sprite import Sprite
from random import randint


class Star(Sprite):
    """Class represent single star at the screen."""
    def __init__(self, bb_game):
        """Initialize star and set starting position"""
        super().__init__()
        self.screen = bb_game.screen
        self.settings = bb_game.settings


        #Download image of star and set rect atributes
        self.image = pygame.image.load('images/star.bmp')
        self.rect = self.image.get_rect()

        #Start each new alien at a random position on the right side of the screen
        self.rect.left = self.screen.get_rect().right
        # The farthest down the screen we'll place the alien is the height
        #   of the screen, minus the height of the alien.
        star_top_max = self.settings.screen_height - self.rect.height
        self.rect.top = randint(0, star_top_max)

        #Store the star exact horizontal position
        self.x = float(self.rect.x)

    def update(self):
        """Move the alien steadily to the left."""
        self.x -= self.settings.alien_speed
        self.rect.x = self.x