# Game Settings below.


class Settings:

    def __init__(self):
        """Initialize games static settings"""
        """Screen settings"""
        self.screen_width = 900
        self.screen_height = 600
        self.bg_color = (230, 230, 230)  # Background color.

        """ Bullet settings """
        #self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        """ Ship Settings """

        self.ship_limit = 3

        """Alien Settings"""

        self.fleet_drop_speed = 2

        # How quickly the game speeds up
        self.speedup_scale = 2

        self.dynamic_settings()

        # Scoring
        self.alien_points = 50
        # How quickly the alien point values increase
        self.score_scale = 1.5

    def dynamic_settings(self):
        self.ship_speed_factor = .2
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 0.1
        self.fleet_direction = 1  # fleet_direction of 1 represents right; -1 represents left.

    def increase_speed(self):
        """Increase speeds settings"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor += self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        #print(self.alien_points)


if __name__ == '__main__':
    print("Go to main file and run from there.")