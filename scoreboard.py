import pygame.font

from pygame.sprite import Sprite,Group

class ShipBoard(Sprite):
    def __init__(self,ai_game,ship_size=0.12):
        super().__init__()
        '''initialize the ship and set its starting position'''
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen_rect
        self.settings = ai_game.settings
        # load the image
        org_image = pygame.image.load('images/ship.png')
        self.image = pygame.transform.scale(org_image, (int(org_image.get_width() * ship_size),
                                                            int(org_image.get_height() * ship_size)))
        self.rect = self.image.get_rect()
        self.rect.left = self.screen_rect.left + 20
        self.rect.top = 20

class ScoreBoard(ShipBoard):
    def __init__(self, ai_game):
        super().__init__(ai_game)
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen_rect
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # font setting for scoring information
        self.text_color = 'white'
        self.font = pygame.font.SysFont(None, 48)

        # prapare the initial score image
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.display_new_record = False
    def prep_score(self):
        '''turn the score into rendered image'''
        # round the numbers
        rounded_score = round(self.stats.score,-1)
        self.score_str = f"Score: {rounded_score:,}"
        self.score_image = self.font.render(self.score_str, True, self.text_color, self.settings.bg_color)

        # display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        '''turn the high score into an image'''
        high_score = round(self.stats.high_score)
        high_score_str = f"High Score: {high_score:,}"
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        # center the high score at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        '''turn the level into a redered image'''
        level_str = str(self.stats.level)
        level_str = f"Level: {level_str}"
        self.level_image = self.font.render(level_str,True,self.text_color,self.settings.bg_color)

        # position the level below score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_lives(self):
        lives_str = str(self.stats.lives)
        lives_str = f"Lives: {lives_str}"
        self.lives_image = self.font.render(lives_str, True, self.text_color, self.settings.bg_color)

        # position the lives on the left side of the screen, slightly above
        self.lives_rect = self.lives_image.get_rect()
        self.lives_rect.left = self.screen_rect.left + 20  # Adjusted the position for better visibility
        self.lives_rect.top = 20

    def display_new_record_msg(self):
        if not self.display_new_record:
            self.ai_game.high_score_sound.play(fade_ms=-2000)
            # Initial settings
            alpha = 255  # Initial alpha value for fully opaque
            duration = 2000  # Display duration in milliseconds
            fade_speed = 2  # Speed of the fade-out effect

            # Display the initial message
            text_surface = self.font.render('New Record!', True, self.text_color)
            text_surface.set_alpha(alpha)
            self.text_img_rect = text_surface.get_rect(center=self.screen_rect.center)
            self.screen.blit(text_surface, self.text_img_rect)
            pygame.display.flip()

            # Wait for the initial duration
            pygame.time.wait(duration)

            # Fade-out loop
            while alpha > 0:
                alpha -= fade_speed
                text_surface.set_alpha(alpha)
                self.screen.blit(text_surface, self.text_img_rect)
                pygame.display.flip()
                pygame.time.delay(5)  # Small delay for a smoother effect

            # Clear the text
            pygame.display.flip()

            self.display_new_record = True

    def show_score(self):
        '''Draw scores and level to the screen.'''
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image,self.high_score_rect)
        self.screen.blit(self.level_image,self.level_rect)

    def check_high_score(self):
        '''check to see if there's a new high score'''
        if self.stats.score > self.stats.high_score:
            self.display_new_record_msg()
            self.stats.high_score = self.stats.score
            self.prep_high_score()

            try:
                with open('highscore.json', 'w') as f:
                    data = f.write(str(self.stats.high_score))
            except FileNotFoundError:
                print("File 'higscore.json' not found")
