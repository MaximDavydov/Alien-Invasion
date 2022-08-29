import sys

import pygame


class KeyGame():
    """Overall class to manage game assets and behavior."""


    def __init__(self):
        # Инициализация и ресурсы
        pygame.init()
        self.screen_width = 1200
        self.screen_height = 600
        self.bg_color = (73, 99, 144)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Simple Screen')

    def run_game(self):
        #запуск основного цикла
        while True:
            self._check_events()
            self._update_screen()

    def _update_screen(self):
        """Redraw screen during each pass though the loop."""
        self.screen.fill(self.bg_color)

        """Make the most recently draws screen visible"""
        pygame.display.flip()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                print(event.key)
                if event.key == pygame.K_q:
                    sys.exit()


if __name__ == '__main__':
    MyGame = KeyGame()
    MyGame.run_game()
