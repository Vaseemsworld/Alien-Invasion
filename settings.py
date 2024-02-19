
class Settings:
    def __init__(self):
        self.screen_width,self.screen_height = 1200,800
        self.bg_color = 'white'
        # Ship
        # self.ship_limit = 3
        # Bullet
        self.bullet_width = 4
        self.bullet_height = 17
        self.bullet_color = 'red'
        self.bullets_allowed = 3
        # alien
        self.fleet_drop_speed = 10
        # how quickly the game speeds up
        self.speedup_scale = 1.1
        # how quickly the alien point values increases
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_limit = 2
        self.ship_speed = 10
        self.alien_speed = 5
        self.bullet_speed = 13
        #fleet direction of 1 represents right; -1 represents left
        self.fleet_direction = 1
        self.alien_points = 50
