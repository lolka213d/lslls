class DatabaseMonitor:
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db
        self.last_values = {}

    def check_updates(self, user_id):
        # Get current values
        user_data = self.db.get_user_data(user_id)
        bp_data = self.db.get_battle_pass_data(user_id)
        farm_data = self.db.get_farm_data(user_id)
        
        # Create unique key for this user
        key = f"user_{user_id}"
        
        # If we have previous values, compare them
        if key in self.last_values:
            old_data = self.last_values[key]
            
            # Check what changed and update
            if old_data['coins'] != user_data['coins']:
                self.bot.send_message(user_id, f"💰 Баланс обновлен: {user_data['coins']} монет")
                
            if old_data['level'] != user_data['level']:
                self.bot.send_message(user_id, f"📊 Уровень повышен до {user_data['level']}!")
                
            if old_data['bp_level'] != bp_data['level']:
                self.bot.send_message(user_id, f"⭐ Уровень боевого пропуска: {bp_data['level']}")
                
            if old_data['farm_level'] != farm_data['level']:
                self.bot.send_message(user_id, f"🏭 Уровень фермы повышен до {farm_data['level']}!")
        
        # Update stored values
        self.last_values[key] = {
            'coins': user_data['coins'],
            'level': user_data['level'],
            'bp_level': bp_data['level'],
            'farm_level': farm_data['level']
        }
