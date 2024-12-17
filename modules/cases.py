class CaseSystem:
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db
        
    def open_case(self, user_id, case_id):
        case = self.db.get_case(case_id)
        if not case:
            return None
            
        user_data = self.db.get_user_data(user_id)
        if user_data['coins'] < case['price']:
            return None
            
        item = self.db.roll_case_item(case_id)
        if item:
            self.db.add_item_to_inventory(user_id, item['id'])
            self.db.remove_coins(user_id, case['price'])
        return item
        
    def get_case_list(self):
        return self.db.get_cases()
