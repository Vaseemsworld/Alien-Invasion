import pygame.font

class Button:
    def __init__(self,ai_game,msg):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # set the dimensions and properties of the button
        self.width, self.height = 200,50
        self.button_color = 'black'
        self.text_color = 'white'
        self.font = pygame.font.SysFont(None,48)

        # build buttons rect object and center it
        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.center = self.screen_rect.center
        # the button msg needs to be prepped only once
        self._prep_msg(msg)

    def _prep_msg(self,msg):
        ''' TURN MSG INTO A RENDERED IMAGE AND CENTER TEXT ON THE BUTTON.'''
        self.msg_image = self.font.render(msg,True,self.text_color,self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        '''draw black button and then draw msg'''
        self.screen.fill(self.button_color,self.rect)
        self.screen.blit(self.msg_image,self.msg_image_rect)