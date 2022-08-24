import sys

import pygame

from settings import Settings
from ship import Ship


class AlienInvasion:
    """Class for control resourses and behavior of game."""

    def __init__(self):
        """Initialize game and create game resourses."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)

        # # Appointment color of background
        # self.bg_color = (230, 230, 230)

    def run_game(self):
        """Launch main cycle of game."""
        while True:
            self._check_events()
            self._update_screen()

    def _check_events(self):
        """Handles key presses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def _update_screen(self):
        """Update image on screen and display new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        pygame.display.flip()


if __name__ == '__main__':
    # Create instance and launch the game.
    ai = AlienInvasion()
    ai.run_game()
