import json
import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button


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

        # Create instance for store game statistics,
        #   and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Create Play button
        self.play_button = Button(self, 'Play')

        #Make the Play button.
        self._make_difficulty_buttons()

        # Load game sounds.
        pygame.mixer.music.load(self.settings.background_music)
        self.bullet_sound = pygame.mixer.Sound(self.settings.bullet_sound)
        self.collision_sound = pygame.mixer.Sound(self.settings.collision_sound)
        self.crash_sound = pygame.mixer.Sound(self.settings.crash_sound)

    def _make_difficulty_buttons(self):
        self.easy_button = Button(self, 'Easy')
        self.medium_button = Button(self, 'Medium')
        self.hard_button = Button(self, 'Hard')

        # Position buttons so they don't all overlap.
        self.easy_button.rect.top = (self.play_button.rect.top + 1.5 * self.easy_button.rect.height)
        self.easy_button.update_msg_position()

        self.medium_button.rect.top = (self.easy_button.rect.top + 1.5 * self.medium_button.rect.height)
        self.medium_button.update_msg_position()

        self.hard_button.rect.top = (self.medium_button.rect.top + 1.5 * self.hard_button.rect.height)
        self.hard_button.update_msg_position()

    def run_game(self):
        """Launch main cycle of game."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        """Handles key presses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # sys.exit()
                self._close_game()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_difficulty_buttons(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self._start_game()

    def _check_difficulty_buttons(self, mouse_pos):
        """Set the appropriate difficulty level."""
        easy_button_clicked = self.easy_button.rect.collidepoint(mouse_pos)
        medium_button_clicked = self.medium_button.rect.collidepoint(mouse_pos)
        hard_button_clicked = self.hard_button.rect.collidepoint(mouse_pos)

        if easy_button_clicked and not self.stats.game_active:
            self.settings.difficulty_level = 'easy'
            self._start_game()
        elif medium_button_clicked and not self.stats.game_active:
            self.settings.difficulty_level = 'medium'
            self._start_game()
        elif hard_button_clicked and not self.stats.game_active:
            self.settings.difficulty_level = 'hard'
            self._start_game()

    def _start_game(self):
        """Start a new game."""
        # Reset the game settings.
        self.settings.initialize_dynamic_settings()

        # Reset the game statistics.
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_image()
        self._reset_game()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

        # Play background music.
        pygame.mixer.music.play(-1)

    def _reset_game(self):
        """Reset stats, fleet, bullets, and ship's position."""
        # Get rid of any remaining aliens and bullets.
        self.aliens.empty()
        self.bullets.empty()

        # Create a new fleet and center the ship.
        self._create_fleet()
        self.ship.center_ship()

    def _check_keydown_events(self, event):
        """Respond to keypresses and mouse events."""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            # Move ship to right.
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            # Move ship to left.
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            # pygame.display.quit()
            self._close_game()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p and not self.stats.game_active:
            self._start_game()


    def _check_keyup_events(self, event):
        """Respond to keypress."""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            # Stop moving ship to right.
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            # Stop moving ship to left.
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            self.bullet_sound.play()
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        # Get rid of bullets that have disappeared.
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # print(len(self.bullets))

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            self.collision_sound.play()
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            self.start_new_level()

    def start_new_level(self):
        """Сlean screen and start a new level."""
        # Destroy existing bullets and create new fleet.
        self.bullets.empty()
        self._create_fleet()
        self.settings.increase_speed()

        # Increase level.
        self.stats.level += 1
        self.sb.prep_level()

        # Rewind music.
        pygame.mixer.music.rewind()

    def _check_alien_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        self.crash_sound.play()
        if self.stats.ship_left > 0:
            # Decrement ships_left, and update scoreboard.
            self.stats.ship_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Creation new fleet and placing ship at the center
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mixer.music.stop()
            pygame.mouse.set_visible(True)

    def _update_aliens(self):
        """Update all positions of aliens in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()

        # Check collision ship - alien
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_alien_bottom()

    def _create_fleet(self):
        """Create fleet of aliens"""
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine count of rows of alien that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create a fleet of alien
        for row_number in range(number_rows):
            for alein_number in range(number_aliens_x):
                self._create_alien(alein_number, row_number)

    def _create_alien(self, alien_number, row_number):
        # Create alien and place it in a row
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Update image on screen and display new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()
            self.easy_button.draw_button()
            self.medium_button.draw_button()
            self.hard_button.draw_button()

        pygame.display.flip()

    def _close_game(self):
        """Save high score and exit."""
        saved_high_score = self.stats.get_saved_high_score()
        if self.stats.high_score > saved_high_score:
            with open('high_score.json', 'w') as f:
                json.dump(self.stats.high_score, f)

        # Stop playing.
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        pygame.mixer.quit()

        sys.exit()


if __name__ == '__main__':
    # Create instance and launch the game.
    ai = AlienInvasion()
    ai.run_game()
