import shelve
class GameStats():
    def __init__(self, ai_s):
        self.ai_s = ai_s
        self.reset_stats()
        self.game_active =False
        self.high_score = 0
                                   
    def reset_stats(self):
        self.ship_left = self.ai_s.ship_limit
        self.score = 0
        self.level = 1
