import sys

import pygame

from settings import Settings
from angry_alien import Alien
from shell import Shell


class BlueSkyGame:
    """Overall class for manage game assets and behavior."""

    def __init__(self):
        """Initialize the game and create a game resources."""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Blue Sky Game')
        self.alien = Alien(self)
        self.shells = pygame.sprite.Group()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self.alien.update()
            self._update_shell()
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

    def _update_screen(self):
        """Redraw screen during each pass though the loop."""
        self.screen.fill(self.settings.bg_color)
        self.alien.blitme()
        for shell in self.shells.sprites():
            shell.draw_shell()
        """Make the most recently draws screen visible"""
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    bsg = BlueSkyGame()
    bsg.run_game()
