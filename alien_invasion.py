from os import environ

environ["PYGAME_HIDE_SUPPORT_PROMPT"] = '1'

import sys
import time
from time import sleep
import pygame
from pygame import mixer
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard, ShipBoard


class AlienInvasion:
    def __init__(self):
        pygame.init()
        mixer.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.size = self.screen.get_size()
        self.screen_width, self.screen_height = self.size
        bg_img = pygame.image.load('images/background.jpg')
        self.background = pygame.transform.scale(bg_img, (self.settings.screen_width, self.settings.screen_height))
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
        self.game_pause = False
        self.ships = pygame.sprite.Group()
        self.prep_ships()
        self.gun_shot = mixer.Sound('sounds/gun shot1.mp3')
        self.bullet_alien_sound = mixer.Sound('sounds/bullet alien explosion.mp3')
        self.lose_life_sound = mixer.Sound('sounds/lose sound1.wav')
        self.lose_sound = mixer.Sound('sounds/lose sound2.wav')
        self.high_score_sound = mixer.Sound('sounds/high score sound.wav')

    def prep_ships(self):
        self.ships.empty()
        for ship_number in range(self.settings.ship_limit):
            ship = ShipBoard(self)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10  # Adjust the y-coordinate as needed
            self.ships.add(ship)

    def run_game(self):
        self._create_fleet()
        while True:
            self._check_event()
            if not self.game_pause:
                if self.game_active and self.stats.lives > 0:
                    self.ship.update()
                    self.bullets.update()
                    self._update_bullets()
                    self._update_alien()
                else:
                    self.game_active = False
                    pygame.mouse.set_visible(True)
                    self.play_button.game_over()
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
            elif event.type == pygame.USEREVENT:
                self.high_score_sound.stop()  # Stop the sound when the timer expires

    def _check_keydown_event(self, event):
        if event.key == pygame.K_q:
            sys.exit()

        if event.key == pygame.K_p:
            if self.game_active and not self.game_pause:
                self.game_pause = True

        if event.key == pygame.K_RETURN:
            self.game_pause = False
            mouse_pos = pygame.mouse.get_pos()
            self._check_play_button(mouse_pos)

        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True

        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True

        if event.key == pygame.K_SPACE:
            if not self.game_pause:
                self._fire_bullet()
                self.gun_shot.play()

    def _check_keyup_event(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        if event.key == pygame.K_SPACE:
            self.gun_shot.stop()

    def _fire_bullet(self):
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _update_bullets(self):
        for bullet in self.bullets.sprites():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._bullet_alien_collision()

    def _bullet_alien_collision(self):
        collision = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collision:
            self.bullet_alien_sound.play()
            for aliens in collision.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self._increase_speed()
            self.stats.level += 1
            self.scoreboard.prep_level()

    def _increase_speed(self):
        self.settings.ship_speed *= self.settings.speedup_scale
        self.settings.bullet_speed *= self.settings.speedup_scale
        self.settings.alien_speed *= self.settings.speedup_scale
        self.settings.alien_points = int(self.settings.alien_points * self.settings.score_scale)

    def _create_fleet(self):
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
            self.lose_life_sound.play()

    def _ship_hit(self):
        if self.settings.ship_limit > 0:
            self.settings.ship_limit -= 1
            self.ships.sprites()[0].kill()  # Remove the current ship
            self.bullets.empty()
            self.aliens.empty()
            self._create_fleet()
            self.prep_ships()  # Create a new ship
            self.clock.tick(1)
        else:
            self._game_inactive()

    def _game_inactive(self):
        self.game_active = False
        self.play_button.game_over()
        self.stats.reset_stats()
        self.play_button.draw_button()
        pygame.mouse.set_visible(True)
        self.settings.initialize_dynamic_settings()

    def _check_aliens_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                self.lose_life_sound.play()
                self.ship.center_ship()
                break

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.stats.reset_stats()
            self._prepare()
            self.settings.initialize_dynamic_settings()
            self.prep_ships()
            self._start_game()

    def _start_game(self):
        if not self.game_active:
            self.stats.reset_stats()
            self.bullets.empty()
            self.aliens.empty()
            self._create_fleet()
            self.ship.center_ship()
            self.game_active = True
            pygame.mouse.set_visible(False)

    def _update_screen(self):
        self.screen.blit(self.background, (0, 0))
        self._prepare()
        self._show()
        pygame.display.flip()

    def _prepare(self):
        self.scoreboard.prep_score()
        self.scoreboard.prep_level()
        self.ships.update()

    def _show(self):
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        self.scoreboard.show_score()

        self.ships.draw(self.screen)

        if not self.game_active:
            self.play_button.draw_button()

        if self.settings.ship_limit == 0:
            self.game_active = False
            self.lose_life_sound.stop()
            self.lose_sound.play()
            self.play_button.game_over()
            self.play_button.draw_button()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
