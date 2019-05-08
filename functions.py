import pygame
import sys
from bullet import Bullet
from alien import Alien
from time import sleep


def check_keydown_events(event, ship, game_settings, screen, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True

    elif event.key == pygame.K_LEFT:
        ship.moving_left = True

    elif event.key == pygame.K_SPACE:
        fire_bullets(game_settings, screen, bullets,  ship)

    elif event.key == pygame.K_ESCAPE:  # Exit if player pushes escape button.
        sys.exit()


def check_keyup_events(ship):

    if ship.moving_right:
        ship.moving_right = False

    if ship.moving_left:
        ship.moving_left = False


def check_events(ship, game_settings, screen, bullets, play_button, stats, aliens, sb):
    """Respond to key presses and mouse clicks."""

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        # When right or left key is pressed below conditions will be executed.
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ship, game_settings, screen, bullets)  # Call the function for key pressed.

        elif event.type == pygame.KEYUP:
            check_keyup_events(ship)  # Call the function for key released.
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y, bullets, game_settings, screen, ship, aliens, sb)


def check_play_button(stats, play_button, mouse_x, mouse_y, bullets, game_settings, screen, ship, aliens, sb):
    """Start a new game when the player clicks Play."""

    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)

    if button_clicked and not stats.game_active:
        game_settings.dynamic_settings()  # Reset the game settings.
        pygame.mouse.set_visible(False)  # Hide the mouse cursor.

        stats.reset_stats()
        stats.game_active = True

    # Reset the scoreboard  images .
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()

    # Empty the list of aliens and bullets.
    aliens.empty()
    bullets.empty()

    # Create a new fleet and center the ship.
    create_fleet(game_settings, screen, aliens, ship)
    ship.center_ship()


def update_screen(game_settings, screen, ship, bullets, aliens,play_button, stats, sb):
    """Update images on the screen and flip to the new screen."""

    screen.fill(game_settings.bg_color)  # Redraw the screen during each pass through the loop.

    for bullet in bullets.sprites():  # Redraw all bullets behind ship and aliens.
        bullet.draw_bullet()

    ship.blitme()

    aliens.draw(screen)
    # Draw the score information.
    sb.show_score()
    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()  # Make the most recently drawn screen visible.


def update_bullets(bullets, aliens, game_settings, screen, ship, stats, sb):
    bullets.update()
    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_collisions(bullets, aliens, game_settings, screen, ship, stats, sb)


def check_bullet_collisions(bullets, aliens, game_settings, screen, ship, stats, sb):
    # Check for any bullets that have hit aliens.
    # If so, get rid of the bullet and the alien.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += game_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    # If all aliens in screen have been shoot down.

    if len(aliens) == 0:
        bullets.empty()  # Destroy existing bullets
        game_settings.increase_speed()  # Speed up the game.
        create_fleet(game_settings, screen, aliens, ship)  # Create new fleet.
        # Increase level.
        stats.level += 1
        sb.prep_level()


def fire_bullets(game_settings, screen, bullets, ship):
    # Create a new bullet and add it to the bullets group.
    if len(bullets) <= game_settings.bullets_allowed:
        new_bullet = Bullet(game_settings, screen,  ship)
        bullets.add(new_bullet)


def get_number_of_aliens_x(game_settings, alien_width):
    available_space_x = game_settings.screen_width - 2 * alien_width
    number_of_aliens_x = int(available_space_x / (2 * alien_width))
    return number_of_aliens_x


def create_fleet(game_settings, screen, aliens, ship):
    """Create a full fleet of aliens."""
    # Create an alien and find the number of aliens in a row.
    # Spacing between each alien is equal to one alien width.
    alien = Alien(game_settings, screen)

    number_aliens_x = get_number_of_aliens_x(game_settings, alien.rect.width)
    number_rows = get_number_rows(game_settings, ship.rect.height, alien.rect.height)

    # Create the rows of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(game_settings, screen, aliens, alien_number, row_number)


def create_alien(game_settings, screen, aliens, alien_number, row_number):

    alien = Alien(game_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def update_aliens(game_settings, aliens, ship, stats, screen, bullets, sb):
    """
    Check if the fleet is at an edge, and then update the postions of all aliens in the fleet.
    """
    check_fleet_edges(game_settings, aliens)
    aliens.update()
    # Look for alien-ship collisions.

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(game_settings, stats, screen, ship, aliens, bullets, sb)
        # print("Ship hit!!!")

    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(game_settings, stats, screen, ship, aliens, bullets, sb)


def change_fleet_direction(game_settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += game_settings.fleet_drop_speed
    game_settings.fleet_direction *= -1


def check_fleet_edges(game_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(game_settings, aliens)
            break


def ship_hit(game_settings, stats, screen, ship, aliens, bullets, sb):
    """Respond to ship being hit by alien."""
    # Decrement ships_left.
    stats.ships_left -= 1
    print(stats.ships_left)
    if stats.ships_left > 0:

        # Update score board.
        sb.prep_ships()
        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()
        # Create a new fleet and center the ship.
        create_fleet(game_settings, screen, aliens, ship)
        ship.center_ship()
        # Pause.

        sleep(0.5)
    else:
        stats.game_active = False
        # Show the mouse cursor.
        pygame.mouse.set_visible(True)


def check_aliens_bottom(game_settings, stats, screen, ship, aliens, bullets, sb):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(game_settings, stats, screen, ship, aliens, bullets, sb)
            break


def get_number_rows(game_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (game_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def check_high_score(stats, sb):
    if stats.score >= stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


if __name__ == '__main__':
    print("Go to main file and run from there.")
