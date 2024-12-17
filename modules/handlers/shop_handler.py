from telebot import types
from config.items import SHOP_ITEMS

class ShopHandler:
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    def handle_shop(self, message):
        text = "🏪 Магазин:\n\n"
        markup = types.InlineKeyboardMarkup(row_width=1)
        
        for item_id, item in SHOP_ITEMS.items():
            text += f"{item['name']} - {item['price']} монет\n"
            markup.add(types.InlineKeyboardButton(
                f"Купить {item['name']}", 
                callback_data=f"buy_item_{item_id}"
            ))
            
        self.bot.reply_to(message, text, reply_markup=markup)

    def handle_shop_callback(self, call):
        if "buy_item" in call.data:
            item_id = int(call.data.split('_')[-1])
            item = SHOP_ITEMS[item_id]
            user = self.db.get_user_data(call.from_user.id)
            
            if user['coins'] >= item['price']:
                self.db.buy_item(call.from_user.id, item_id, item['price'])
                self.bot.answer_callback_query(
                    call.id,
                    f"✅ Вы купили {item['name']}!",
                    show_alert=True
                )
            else:
                self.bot.answer_callback_query(
                    call.id,
                    "💰 Недостаточно монет!",
                    show_alert=True
                )
