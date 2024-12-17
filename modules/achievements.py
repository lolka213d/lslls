class Achievements:
    def __init__(self, db):
        self.db = db
        self.achievements = {
            'size_master': {
                'name': 'Мастер размера',
                'levels': {
                    1: {'requirement': 10, 'reward_coins': 100},
                    2: {'requirement': 25, 'reward_coins': 250},
                    3: {'requirement': 50, 'reward_coins': 500}
                }
            },
            'rich_player': {
                'name': 'Богач',
                'levels': {
                    1: {'requirement': 1000, 'reward_coins': 100},
                    2: {'requirement': 5000, 'reward_coins': 500},
                    3: {'requirement': 10000, 'reward_coins': 1000}
                }
            },
            'farm_king': {
                'name': 'Король фермы',
                'levels': {
                    1: {'requirement': 100, 'reward_coins': 50},
                    2: {'requirement': 500, 'reward_coins': 250},
                    3: {'requirement': 1000, 'reward_coins': 500}
                }
            }
        }
    
    def check_achievements(self, user_id):
        user_data = self.db.get_user_data(user_id)
        completed = []
        
        for ach_id, achievement in self.achievements.items():
            progress = self.get_achievement_progress(user_id, ach_id)
            for level, data in achievement['levels'].items():
                if progress >= data['requirement']:
                    if self.db.complete_achievement(user_id, ach_id, level):
                        completed.append({
                            'name': achievement['name'],
                            'level': level,
                            'reward': data['reward_coins']
                        })
        
        return completed
    
    def get_achievement_progress(self, user_id, achievement_id):
        user_data = self.db.get_user_data(user_id)
        
        if achievement_id == 'size_master':
            return user_data['dick_size']
        elif achievement_id == 'rich_player':
            return user_data['coins']
        elif achievement_id == 'farm_king':
            return user_data['total_mined']
        
        return 0
