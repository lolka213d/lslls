from telebot import types
from config.items import ITEMS

class InventoryHandler:
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    def handle_inventory(self, message):
        inventory = self.db.get_inventory(message.from_user.id)
        
        if not inventory:
            return self.bot.reply_to(message, "🎒 Ваш инвентарь пуст!")
            
        text = "🎒 Ваш инвентарь:\n\n"
        markup = types.InlineKeyboardMarkup(row_width=2)
        
        for item in inventory:
            item_data = ITEMS[item['item_id']]
            text += f"{item_data['name']} x{item['quantity']}\n"
            markup.add(types.InlineKeyboardButton(
                f"Использовать {item_data['name']}", 
                callback_data=f"use_item_{item['item_id']}"
            ))
            
        self.bot.reply_to(message, text, reply_markup=markup)

    def handle_inventory_callback(self, call):
        if "use_item" in call.data:
            item_id = int(call.data.split('_')[-1])
            if self.db.use_item(call.from_user.id, item_id):
                item_data = ITEMS[item_id]
                self.bot.answer_callback_query(
                    call.id,
                    f"✅ {item_data['name']} использован!",
                    show_alert=True
                )
            else:
                self.bot.answer_callback_query(
                    call.id,
                    "❌ Предмет не найден в инвентаре!",
                    show_alert=True
                )
