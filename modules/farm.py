class Farm:
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db
        
    def collect(self, user_id):
        farm_data = self.db.get_farm_data(user_id)
        if not farm_data:
            self.db.create_farm(user_id)
            farm_data = self.db.get_farm_data(user_id)
            
        coins = self.calculate_income(farm_data)
        self.db.collect_farm_income(user_id, coins)
        return coins
        
    def upgrade(self, user_id):
        farm_data = self.db.get_farm_data(user_id)
        upgrade_cost = self.calculate_upgrade_cost(farm_data['level'])
        
        if self.db.spend_coins(user_id, upgrade_cost):
            self.db.upgrade_farm(user_id)
            return True
        return False
        
    def calculate_income(self, farm_data):
        time_passed = (datetime.now() - farm_data['last_collection']).total_seconds()
        hours = time_passed / 3600
        return int(hours * farm_data['production_rate'])
        
    def calculate_upgrade_cost(self, current_level):
        return FARM_UPGRADE_BASE_PRICE * current_level
