class LevelSystem:
    def __init__(self, db):
        self.db = db
        self.level_thresholds = {
            1: 0,
            2: 100,
            3: 250,
            4: 500,
            5: 1000,
            6: 2000,
            7: 4000,
            8: 8000,
            9: 16000,
            10: 32000
        }
        
    def check_level_up(self, user_id):
        user_data = self.db.get_user_data(user_id)
        current_level = user_data['level']
        exp = user_data['experience']
        
        for level, threshold in self.level_thresholds.items():
            if exp >= threshold and level > current_level:
                self.level_up(user_id, level)
                return {
                    'new_level': level,
                    'rewards': self.get_level_rewards(level)
                }
        return None
    
    def get_level_rewards(self, level):
        rewards = {
            'coins': level * 100,
            'energy_max': level,
            'mining_power': level // 2
        }
        return rewards
    
    def level_up(self, user_id, new_level):
        rewards = self.get_level_rewards(new_level)
        self.db.process_level_up(user_id, new_level, rewards)
