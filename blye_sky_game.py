import sys

import pygame

from settings import Settings
from angry_alien import Alien
from shell import Shell
from star import Star
from second_game_stats import GameStats

from random import random



class BlueSkyGame:
    """Overall class for manage game assets and behavior."""

    def __init__(self):
        """Initialize the game and create a game resources."""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Blue Sky Game')

        # Create an instance to store game statistics.
        self.stats = GameStats(self)

        self.alien = Alien(self)
        self.shells = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()


    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            if self.stats.game_active:
                self._create_starfall()
                self.alien.update()
                self._update_shell()
                self._update_stars()
            self._update_screen()

    def _check_events(self):
        """Watch for keyboard and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_down(event)
            elif event.type == pygame.KEYUP:
                self._check_up(event)

    def _check_down(self, event):
        # ответ на нажатие изменяем флаг на движение непрерывное
        if event.key == pygame.K_RIGHT:
            self.alien.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.alien.moving_left = True
        elif event.key == pygame.K_UP:
            self.alien.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.alien.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._shell_fire()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_up(self, event):
        # ответ на отжатие клавиши изменяе флаг на стоп
        if event.key == pygame.K_RIGHT:
            self.alien.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.alien.moving_left = False
        elif event.key == pygame.K_UP:
            self.alien.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.alien.moving_down = False

    def _shell_fire(self):
        if len(self.shells) < self.settings.bullets_allowed:
            new_shell = Shell(self)
            self.shells.add(new_shell)

    def _update_shell(self):
        """Уничтожение пуль, которые вышли за рамки"""
        self.shells.update()

        for shell in self.shells.copy():
            if shell.rect.left >= self.screen.get_rect().right:
                self.shells.remove(shell)
            print(len(self.shells))

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Check whether any bullets have hit an alien."""
        collision = pygame.sprite.groupcollide(self.shells, self.stars, False, True)

    def _create_starfall(self):
        """Create a starfall at the screen"""
        #create a starfall and find aliens in a row
        #spacing between each star is zero
        if random() < self.settings.alien_frequency:
            star = Star(self)
            self.stars.add(star)
            print((len(self.stars)))
        # star_width, star_height = star.rect.size
        # alien = Alien(self)
        # alien_width, alien_height = alien.rect.size
        #
        # available_space_x = self.settings.screen_width - star_width - alien_width * 2
        #
        # number_stars_x = available_space_x // (2 *star_width)
        #
        # #check count rows in a starfall
        # available_space_y = self.settings.screen_height
        # number_rows = available_space_y // (2 * star_height)
        #
        # for row_number in range(number_rows):
        #     for star_num in range(number_stars_x):
        #         self._create_star(star_num, row_number)

    def _update_stars(self):
        """Update star position, and look for collisions with alien"""
        self.stars.update()

        if pygame.sprite.spritecollideany(self.alien, self.stars):
            self._alien_hit()

        # Look for aliens that have hit the left edge of the screen.
        self._check_stars_left_edge()

    def _check_stars_left_edge(self):
        """Respond to aliens that have hit left edge of the screen.
                Treat this the same as the ship getting hit.
                """
        for star in self.stars.sprites():
            if star.rect.left < 0:
                self._alien_hit()
                break

    def _alien_hit(self):
        """Respond to an star hitting the alien"""
        if self.stats.alien_left > 0:
            #Decrease alien left
            self.stats.alien_left -= 1

            #Get rid of any remaining aliens and bullets
            self.stars.empty()
            self.shells.empty()

            #center the alien
            self.alien.center_alien()
        else:
            self.stats.game_active = False

    def _create_star(self, star_num, row):
        star = Star(self)
        alien = Alien(self)
        star_width, star_height = star.rect.size
        alien_width, alien_height = alien.rect.size
        star.x = star_width + 2 * star_width * star_num + alien_width * 2
        star.rect.x = star.x
        star.rect.y = star.rect.height + 2 * star.rect.height * row
        self.stars.add(star)

    def _update_screen(self):
        """Redraw screen during each pass though the loop."""
        self.screen.fill(self.settings.bg_color)
        self.alien.blitme()
        for shell in self.shells.sprites():
            shell.draw_shell()
        """Make the most recently draws screen visible"""
        self.stars.draw(self.screen)
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    bsg = BlueSkyGame()
    bsg.run_game()
