import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self,ai_game,alien_size = 0.12):
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen_rect
        self.settings = ai_game.settings

        #load the image
        org_img = pygame.image.load('images/alien3.png')
        self.image = pygame.transform.scale(org_img,(int(org_img.get_width()*alien_size),
                                                     int(org_img.get_height()*alien_size)))
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = 40+self.rect.height

        self.x = float(self.rect.x)

    def blitme(self):
        self.screen.blit(self.image,self.rect)

    def check_edges(self):
        # if self.rect.right >= self.screen_rect.right or self.rect.left <=0:
        #     return True
        # else:
        #     return False

        # this approach is more concise
        return self.rect.right >= self.screen_rect.right or self.rect.left <= 0

    def update(self):
        self.rect.x += self.settings.alien_speed*self.settings.fleet_direction

