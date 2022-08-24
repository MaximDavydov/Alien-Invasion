import pygame

class Alien:
    """Class for alien control."""

    def __init__(self, bb_game):
        """Initialize the bird and set its starting position."""
        self.screen = bb_game.screen
        self.screen_rect = bb_game.screen.get_rect()

        #Load the alien image and get it rec
        self.image = pygame.image.load('images/angry_alien.bmp')
        self.rect = self.image.get_rect()

        # Start each new bird at the center of the screen.
        self.rect.center = self.screen_rect.center

    def blitme(self):
        """Draw alien in current position."""
        self.screen.blit(self.image, self.rect)
