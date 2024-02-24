import json
import os  # Import the os module to handle file existence checks

class GameStats:
    '''track statistics for game'''
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.score = 0
        self.level = 1
        self.lives = 3
        self.high_scores()

    def high_scores(self):
        # Check if the file exists before attempting to load data
        if os.path.exists('highscore.json'):
            with open('highscore.json', 'r') as f:
                data = json.load(f)
            self.high_score = data
        else:
            # Set a default high score if the file doesn't exist
            self.high_score = 0

    def reset_stats(self):
        # Use consistent attribute name (lives instead of ship_left)
        self.lives = self.settings.ship_limit
        self.score = 0
        self.level = 1
