import sys

import pygame

from settings import Settings


class AlienInvasion:
    """Class for control resourses and behavior of game."""

    def __init__(self):
        """Initialize game and create game resourses."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # # Appointment color of background
        # self.bg_color = (230, 230, 230)

    def run_game(self):
        """Launch main cycle of game."""
        while True:
            # Event tracking keyboard and mouse.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            #On each pass of loop redrawn screen
            self.screen.fill(self.settings.bg_color)

            # Display last drawn screen.
            pygame.display.flip()


if __name__ == '__main__':
    # Create instance and launch the game.
    ai = AlienInvasion()
    ai.run_game()
