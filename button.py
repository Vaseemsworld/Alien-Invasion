import sys
import time

import pygame.font


class Button:
    def __init__(self, ai_game, msg):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # set the dimensions and properties of the play button
        self.width, self.height = 200, 50
        self.button_color = (255,0,0)
        self.text_color = 'white'
        self.font = pygame.font.SysFont(None, 48)

        # build buttons rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        # the button msg needs to be prepped only once
        self._prep_msg(msg)


        # game over button
        self.game_width, self.game_height = 300, 70
        self.game_over_image_rect = pygame.Rect(0, 0, self.game_width, self.game_height)

    def game_over(self):
        self.game_over_txt_image = self.font.render('Game Over', True, self.text_color, self.button_color)
        # self.game_over_image_rect = self.game_over_image.get_rect()
        self.game_over_txt_image_rect = self.game_over_txt_image.get_rect()
        self.game_over_txt_image_rect.center = self.game_over_image_rect.center
        self.game_over_image_rect.centerx = self.screen_rect.centerx
        self.game_over_image_rect.top = self.rect.bottom + 20

        # Create a surface with the button color
        self.screen.fill(self.button_color,self.game_over_image_rect)

        # Blit the game over image onto the screen
        self.screen.blit(self.game_over_txt_image, self.game_over_txt_image_rect)


    def _prep_msg(self, msg):
        ''' TURN MSG INTO A RENDERED IMAGE AND CENTER TEXT ON THE BUTTON.'''
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        '''draw black button and then draw msg'''
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)


