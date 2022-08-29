import sys

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """Class for control resourses and behavior of game."""

    def __init__(self):
        """Initialize game and create game resourses."""
        pygame.init()
        self.settings = Settings()

        # settings for full screen mode.
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

    def run_game(self):
        """Launch main cycle of game."""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()

    def _check_events(self):
        """Handles key presses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to keypresses and mouse events."""
        if event.key == pygame.K_RIGHT:
            # Move ship to right.
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # Move ship to left.
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            pygame.display.quit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to keypress."""
        if event.key == pygame.K_RIGHT:
            # Stop moving ship to right.
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            # Stop moving ship to left.
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        # Get rid of bullets that have disappeared.
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        #print(len(self.bullets))

    def _create_fleet(self):
        """Create fleet of aliens"""
        #Create alien
        alien = Alien(self)
        self.aliens.add(alien)

    def _update_screen(self):
        """Update image on screen and display new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        pygame.display.flip()


if __name__ == '__main__':
    # Create instance and launch the game.
    ai = AlienInvasion()
    ai.run_game()
