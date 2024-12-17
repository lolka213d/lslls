class Inventory:
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db
        
    def show_inventory(self, user_id):
        items = self.db.get_user_inventory(user_id)
        if not items:
            return "🎒 Ваш инвентарь пуст!"
            
        text = "🎒 Ваш инвентарь:\n\n"
        for item in items:
            text += f"• {item['name']} x{item['quantity']}\n"
        return text
        
    def use_item(self, user_id, item_id):
        item = self.db.get_item(item_id)
        if not item:
            return False
            
        if self.db.remove_item_from_inventory(user_id, item_id):
            self.apply_item_effect(user_id, item)
            return True
        return False
        
    def apply_item_effect(self, user_id, item):
        if item['type'] == 'boost':
            self.db.add_dick_size(user_id, item['effect_value'])
        elif item['type'] == 'farm':
            self.db.boost_farm(user_id, item['effect_value'])
