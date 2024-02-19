import pygame.font

class ScoreBoard:
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen_rect
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # font setting for scoring information
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # prapare the initial score image
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_lives()
    def prep_score(self):
        '''turn the score into rendered image'''
        # round the numbers
        rounded_score = round(self.stats.score,-1)
        self.score_str = f"Score : {rounded_score:,}"
        # self.score_str = str(self.stats.score)
        self.score_image = self.font.render(self.score_str, True, self.text_color, self.settings.bg_color)

        # display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        '''turn the high score into an image'''
        high_score = round(self.stats.high_score)
        high_score_str = f"High Score : {high_score:,}"
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        # center the high score at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        '''turn the level into a redered image'''
        level_str = str(self.stats.level)
        level_str = f"Level : {level_str}"
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

    def show_score(self):
        '''Draw scores and level to the screen.'''
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image,self.high_score_rect)
        self.screen.blit(self.level_image,self.level_rect)
        self.screen.blit(self.lives_image,self.lives_rect)
    def check_high_score(self):
        '''check to see if there's a new high score'''
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

            with open('highscore.json', 'w') as f:
                data = f.write(str(self.stats.high_score))