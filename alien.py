import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Class for represent single alien in the fleet."""

    def __init__(self, ai_game):
        """Initialise alien and set its starting position"""
        super().__init__()
        self.screen = ai_game.screen

        #Download imagine of alien and set it rect atribute
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        #Store the alien exact horizontal position
        self.x = float(self.rect.x)