class Settings():
    def __init__(self):
        self.screen_width = 1250
        self.screen_height = 625
        self.bg_color = (230, 230, 230)

        #ship settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60,60,60
        self.bullet_allowed = 3
        self.fleet_drop_speed = 13
        self.ship_limit = 3
        self.speedup_scale = 1.5
        self.initialize_dynamic_setting()
        self.score_scale = 1.5

    def initialize_dynamic_setting(self):
            self.ship_speed_factor = 1.5
            self.bullet_speed_factor = 3
            self.alien_speed_factor = 1.5
            self.fleet_direction = 1
            self.alien_points = 50

    def increase_speed(self):
            self.ship_speed_factor *= self.speedup_scale
            self.bullet_speed_factor *= self.speedup_scale
            self.alien_speed_factor *= self.speedup_scale
            self.aliens_points = int(self.alien_points*self.score_scale)
            
