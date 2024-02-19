import sys
from time import sleep
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard


class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        # self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        # update the game to full screen
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption('Alien Invasion')
        self.stats = GameStats(self)
        self.scoreboard = ScoreBoard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.game_active = False
        self.play_button = Button(self, 'Play')

    def run_game(self):
        ''' Note - don't put _create_fleet func in the loop bcs it create aliens every time the loop
        run and in game loop run unlimited times and make game slow'''
        # create alien fleet
        self._create_fleet()
        while True:
            self._check_event()
            if self.game_active:
                self.ship.update()
                self.bullets.update()
                self._update_bullets()
                self._update_alien()

            self._update_screen()
            self.clock.tick(60)


    def _check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_event(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_event(self, event):
        if event.key == pygame.K_q:
            sys.exit()

        if event.key == pygame.K_p:
            self._start_game()

        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True

        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True

        if event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_event(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        # create a new bullet and add it to the bullets group
        # limits the bullets allowed at once
        # if (len(self.bullets)) < self.settings.bullets_allowed:
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _update_bullets(self):
        # get rid of bullets that disappers from the screen
        for bullet in self.bullets.sprites():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._bullet_alien_collision()

    def _bullet_alien_collision(self):
        # check for any bullet that have hit alien if so git rid of them
        collision = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collision:
            for aliens in collision.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self._increase_speed()
            self.stats.level +=1
            self.scoreboard.prep_level()

    def _increase_speed(self):
        '''increase speed settings and alien point values'''
        self.settings.ship_speed *= self.settings.speedup_scale
        self.settings.bullet_speed *= self.settings.speedup_scale
        self.settings.alien_speed *= self.settings.speedup_scale
        self.settings.alien_points = int(self.settings.alien_points * self.settings.score_scale)
    def _create_fleet(self):
        # create fleet
        alien = Alien(self)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        current_x = alien_width
        current_y = alien_height
        while current_y < self.settings.screen_height - 4 * alien_height:
            while current_x < self.settings.screen_width - 2 * alien_width:
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        # create one alien
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_alien(self):
        self._check_fleet_edges()
        self.aliens.update()
        self._alien_ship_collision()
        self._check_aliens_bottom()

    def _alien_ship_collision(self):
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

    def _ship_hit(self):
        # empty bullets and aliens groups
        if self.settings.ship_limit > 0:
            self.settings.ship_limit -= 1
            self.stats.lives -= 1
            self.scoreboard.prep_lives()
            self.bullets.empty()
            self.aliens.empty()
            self._create_fleet()
            self.ship.center_ship()
            # Pause
            sleep(1)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)
            self.settings.initialize_dynamic_settings()

    def _check_aliens_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

    def _check_play_button(self, mouse_pos):
        ''' Start a new game when the player clicks play'''
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # reset the game settings
            self.stats.reset_stats()
            self.stats.score = 0
            self.stats.level = 1
            self.stats.lives = 3
            self.scoreboard.prep_score()
            self.scoreboard.prep_level()
            self.scoreboard.prep_lives()
            self.settings.initialize_dynamic_settings()
            self._start_game()

    def _start_game(self):
        # reset the game stats
        if not self.game_active:
            self.stats.reset_stats()
            self.game_active = True

            # get rid of any remaining bullet or aliens
            self.bullets.empty()
            self.aliens.empty()

            # create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # hiding the mouse curser
            pygame.mouse.set_visible(False)

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.scoreboard.prep_score()
        self.scoreboard.prep_level()
        self.scoreboard.prep_lives()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        self.scoreboard.show_score()
        # drtaw the play button if game is inactive
        if not self.game_active:
            self.play_button.draw_button()
        # flip the screen
        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
