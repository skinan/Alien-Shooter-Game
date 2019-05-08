
class GameStats():
    """Track statistics for Alien Invasion."""
    def __init__(self, game_settings):
        """Initialize statistics."""
        self.game_settings = game_settings
        self.high_score = int()  # High Scores should never be reset.
        self.level = 1  # Game level.
        self.reset_stats()

        # Start Alien Shooter in an active state.
        self.game_active = False

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.game_settings.ship_limit
        self.score = 0
        self.level = 1


if __name__ == '__main__':
    print("Go to main file and run from there.")
