
class Settings:
    def __init__(self):
        self.screen_width,self.screen_height = 1920,1080
        self.bg_color = 'black'
        # Bullet
        self.bullet_width = 5
        self.bullet_height = 18
        self.bullet_color = 'red'
        self.bullets_allowed = 3
        # alien
        self.fleet_drop_speed = 12
        # how quickly the game speeds up
        self.speedup_scale = 1.1
        # how quickly the alien point values increases
        self.score_scale = 1.2
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_limit = 3
        self.ship_speed = 12
        self.alien_speed = 7
        self.bullet_speed = 16
        #fleet direction of 1 represents right; -1 represents left
        self.fleet_direction = 1
        self.alien_points = 50
