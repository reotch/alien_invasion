class Settings:
    '''This class stores all settings for Invasion!'''

    def __init__(self):
        '''Initialize game static settings'''
        # Screen settings
        # Current 3:2 aspect ratio
        self.screen_width = 1152
        self.screen_height = 768
        self.bg_color = (10, 10, 10)

        # Ship settings
        self.ships_limit = 3

        # Laser settings
        self.laser_width = 5
        self.laser_height = 45
        self.laser_color = (12, 255, 110)
        self.max_shots = 3

        # Alien settings
        self.fleet_drop_speed = 10

        # Game speed-up settings
        self.speedup_scale = 1.1

        # Game scoring point value increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        '''Initialize settings that change throughout the game'''
        self.ship_speed = 1.5
        self.laser_speed = 1.5
        self.alien_speed = 1.0

        # Fleet direction of 1 is to the right, -1 is to the left
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        '''Increase speed and scoring settings'''
        self.ship_speed *= self.speedup_scale
        self.laser_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)