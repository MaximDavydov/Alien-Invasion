import pygame

class Ship():
    """Class for ship control."""
    def __init__(self, ai_game):
        """Ship initialising and set his start position."""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        #Download ship image and take rectangle.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        #Each new ship emerge on the botoom edge of the screen
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        """Draw ship in current position."""
        self.screen.blit(self.image, self.rect)