import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from laser import Laser
from alien import Alien

class AlienInvasion:
    '''Overall class to manage game assets and behavior.'''

    def __init__(self):
        '''Initialize game, create game resources'''
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        # Fullscreen code...didn't work on the dell
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Invasion!")

        # Create instance to store game stats
        self.stats = GameStats(self)

        # Create instance of scoreboard
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.lasers = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Create instance of play button
        self.play_button = Button(self, 'Play')

    def run_game(self):
        '''Start the main loop for the game'''
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_lasers()
                self._update_aliens()
            self._update_screen()

    def _check_events(self):
        '''Respond to keypresses and mouse events'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        '''Respond to keydown events'''
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            # ship moves right
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            # ship moves left
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_laser()
        elif event.key == pygame.K_UP:
            self._start_game()
        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
            sys.exit()

    def _check_keyup_events(self, event):
        '''Respond to key release events'''
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = False

    def _check_play_button(self, mouse_pos):
        '''Start a new game when the player clicks Play button'''
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self._start_game()

    def _start_game(self):
        '''A method that includes mouse and keydown to start the game'''
        # Reset game stats
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()

        # Reset game settings
        self.settings.initialize_dynamic_settings()

        # Dispose of remaining alien wessels and lasers
        self.aliens.empty()
        self.lasers.empty()

        # Create a new fleet and center ship
        self._create_fleet()
        self.ship.center_ship()

        # Hide mouse pointer
        pygame.mouse.set_visible(False)

    def _fire_laser(self):
        '''Create a new laser, add it to the laser group'''
        # number of lasers limited by settings
        if len(self.lasers) < self.settings.max_shots:
            new_laser = Laser(self)
            self.lasers.add(new_laser)

    def _update_lasers(self):
        '''Update position of lasers and get rid of off-screen lasers'''
        self.lasers.update()

        # Delete laser blasts when they have traveled off screen
        for laser in self.lasers.copy():
            if laser.rect.bottom <= 0:
                self.lasers.remove(laser)
        # print(len(self.lasers))

        # Check collisions between lasers and alien wessels
        self._check_laser_alien_collisions()

    def _ship_hit(self):
        '''Respond to ship being hit by alien wessel'''
        if self.stats.ships_left > 0:
            # Decrement ships remaining and scoreboard
            self.stats.ships_left -= 1
            self.sb.prep_ships()
        
            # Remove any remaining alien wessels and lasers
            self.aliens.empty()
            self.lasers.empty()

            # Create new fleet, center ship
            self._create_fleet()
            self.ship.center_ship()

            # Pause for a moment
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_laser_alien_collisions(self):
        '''Respond to lasers hitting alien wessels'''
        # If collision, get rid of both laser and alien wessel
        collisions = pygame.sprite.groupcollide(
                self.lasers, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        # If aliens are defeated
        if not self.aliens:
            # Destroy existing lasers, create new fleet
            self.lasers.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level
            self.stats.level += 1
            self.sb.prep_level()
    
    def _check_aliens_bottom(self):
        '''Check if an alien wessel has made contact with bottom of screen'''
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _update_screen(self):
        '''Update images on the screen, flip to the new screen'''
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for laser in self.lasers.sprites():
            laser.draw_laser()
        self.aliens.draw(self.screen)

        # Draw Scoreboard
        self.sb.show_score()

        # Draw Play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible
        pygame.display.flip()

    def _create_fleet(self):
        '''Create a fleet of the alien wessels'''
        # Make an alien ship, find the number of aliens that fit a row
        # Spacing between aliens is equal to one alien width
        alien = Alien(self) # This alien is not on the screen, but a template for aliens that are
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
            
    def _create_alien(self, alien_number, row_number):
        '''Create an alien wessel, place it in the row'''
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        '''Check if the fleet is an edge then 
            update the positions of all alien 
            wessels in the fleet'''
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-to-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for alien-to-bottom collisions
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        '''Respond if alien wessels have reached an edge of the screen'''
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        '''Drop the entire fleet and change the fleet direction'''
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

if __name__ == '__main__':
    # Make a game instance, run the game
    ai = AlienInvasion()
    ai.run_game()
