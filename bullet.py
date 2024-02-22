import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self,ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen_rect
        self.settings = ai_game.settings
        self.ship = ai_game.ship
        self.rect = pygame.Rect(0,0,self.settings.bullet_width,self.settings.bullet_height)
        self.rect.midtop = self.ship.rect.midtop

        # Store the bullets position as a float
        self.y = float(self.rect.y)

    def update(self):
        # move bullet on the screen
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        # drawing the bullet to the screen
        pygame.draw.rect(self.screen,self.settings.bullet_color,self.rect)

