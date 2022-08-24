import sys

import pygame

from settings import Settings
from angry_alien import Alien


class BlueSkyGame:
    """Overall class for manage game assets and behavior."""

    def __init__(self):
        """Initialize the game and create a game resources."""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Blue Sky Game')

        self.alien = Alien(self)

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self._update_screen()

    def _check_events(self):
        """Watch for keyboard and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def _update_screen(self):
        """Redraw screen during each pass though the loop."""
        self.screen.fill(self.settings.bg_color)
        self.alien.blitme()

        """Make the most recently draws screen visible"""
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    bsg = BlueSkyGame()
    bsg.run_game()