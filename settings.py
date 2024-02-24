import pygame.color

class Settings:
    def __init__(self):
        self.screen_width, self.screen_height = 1920, 1080
        self.bg_color = pygame.color.Color('black')

        # Bullet
        self.bullet_width = 6
        self.bullet_height = 20
        self.bullet_color = pygame.color.Color('red')
        self.bullets_allowed = 3

        # Alien
        self.fleet_drop_speed = 12

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        # How quickly the alien point values increase
        self.score_scale = 1.2
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        # Ship settings
        self.ship_limit = 3
        self.ship_speed = 12

        # Alien settings
        self.alien_speed = 8
        self.alien_points = 50

        # Bullet settings
        self.bullet_speed = 16

        # Fleet direction of 1 represents right; -1 represents left
        self.fleet_direction = 1
