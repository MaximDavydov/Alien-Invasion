class GameStats:
    """Track statistics for the game."""

    def __init__(self, bb_game):
        """Initialize statistics."""
        self.settings = bb_game.settings
        self.reset_stats()

        #Start game in an active state.
        self.game_active = True

    def reset_stats(self):
        """Initialize statistics that can chenge during the game."""
        self.alien_left = self.settings.ship_limit