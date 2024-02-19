import json


class GameStats:
    '''track statistics for game'''
    def __init__(self,ai_game):
        self.settings = ai_game.settings
        # high score should never be reset
        # self.high_score = 0
        self.score = 0
        self.level = 1
        self.lives = 3
        self.high_scores()
    def high_scores(self):
        with open('highscore.json','r') as f:
            data = json.load(f)
        self.high_score = data
    def reset_stats(self):
        self.ship_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
        self.lives = 3

