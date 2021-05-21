class GameStats:
    '''Tracks stats for Invasion'''

    def __init__(self, ai_game):
        '''Initialize stats'''
        self.settings = ai_game.settings
        self.reset_stats()

        # High score -- never reset!
        self.high_score = 0

        # Start Invasion! in an inactive state
        self.game_active = False

    def reset_stats(self):
        '''Initialize stats that can change in game'''
        self.ships_left = self.settings.ships_limit
        self.score = 0
        self.level = 1