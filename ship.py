import pygame

class Ship:
    def __init__(self, ai_game, ship_size=0.23):
        '''initialize the ship and set its starting position'''
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen_rect
        self.settings = ai_game.settings
        # load the image
        org_image = pygame.image.load('images/ship3.png')
        self.image = pygame.transform.scale(org_image, (int(org_image.get_width() * ship_size),
                                                        int(org_image.get_height() * ship_size)))
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom

        # store the float value for the ship's exact horizontal position
        self.x = float(self.rect.x)

        self.moving_right = False
        self.moving_left = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.rect.x = self.x

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom