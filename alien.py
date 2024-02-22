import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    def __init__(self, ai_game, alien_size=0.09):
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen_rect
        self.settings = ai_game.settings

        # load the image
        alien_img = pygame.image.load('images/alien2.png')
        self.image = pygame.transform.scale(alien_img, (int(alien_img.get_width() * alien_size),
                                                      int(alien_img.get_height() * alien_size)))
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        return self.rect.right >= self.screen_rect.right or self.rect.left <= 0

    def update(self):
        self.rect.x += self.settings.alien_speed * self.settings.fleet_direction
