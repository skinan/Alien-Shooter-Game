import pygame

from pygame.sprite import Group
from settings import Settings
from ship import Ship
import functions as gf
from alien import Alien
from gameStats import GameStats
from button import Button
from scoreboard import ScoreBoard


def run_game():

    pygame.init()  # Initialize game and create a screen object.

    game_settings = Settings()  # Make it constructor.Make an instance.

    screen = pygame.display.set_mode((game_settings.screen_width, game_settings.screen_height))  # Set screen size
    alien = Alien(game_settings, screen)  # Make Alien.
    pygame.display .set_caption("Alien Shooter")

    # Make the Play button.
    play_button = Button(game_settings, screen, "Play")  # Make Button.

    ship = Ship(screen, game_settings)  # Make a a ship.

    stats = GameStats(game_settings)  # Create an instance to store game statistics.

    sb = ScoreBoard(game_settings, screen, stats)
    bullets = Group()  # Make a group of bullets.
    aliens = Group()  # # Make a group of aliens.

    # Create the fleet of aliens.
    gf.create_fleet(game_settings, screen, aliens, ship)

    # Start main loop for the game.
    while True:
        # Watch Keyboard and Mouse events.
        gf.check_events(ship, game_settings, screen, bullets, play_button, stats, aliens, sb)
        if stats.game_active:
            ship.update()
            gf.update_bullets(bullets, aliens, game_settings, screen, ship, stats, sb)  # Updating bullets.
            gf.update_aliens(game_settings, aliens, ship, stats, screen, bullets, sb)  # Update aliens.
        # Updating or loading the screen.
        gf.update_screen(game_settings, screen, ship, bullets, aliens, play_button, stats, sb)


if __name__ == '__main__':
    run_game()

