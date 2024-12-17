from telebot import types
from config.config import ADMIN_IDS

class AdminHandler:
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    def handle_admin(self, message):
        if message.from_user.id in ADMIN_IDS:
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(
                types.InlineKeyboardButton("💰 Выдать монеты", callback_data="admin_give_coins"),
                types.InlineKeyboardButton("🎁 Выдать предмет", callback_data="admin_give_item"),
                types.InlineKeyboardButton("⚡️ Выдать энергию", callback_data="admin_give_energy"),
                types.InlineKeyboardButton("⭐️ Выдать премиум", callback_data="admin_give_premium"),
                types.InlineKeyboardButton("📊 Статистика", callback_data="admin_stats")
            )
            self.bot.reply_to(message, "👑 Админ-панель:", reply_markup=markup)
        else:
            self.bot.reply_to(message, "⛔️ У вас нет доступа к админ-панели!")

    def handle_admin_callback(self, call):
        if call.from_user.id not in ADMIN_IDS:
            return self.bot.answer_callback_query(call.id, "⛔️ У вас нет доступа!", show_alert=True)
            
        if call.data == "admin_give_coins":
            msg = self.bot.send_message(call.from_user.id, "💰 Введите: /give_coins [ID] [количество]")
            self.bot.register_next_step_handler(msg, self.admin_give_coins)
            
        elif call.data == "admin_give_item":
            msg = self.bot.send_message(call.from_user.id, "🎁 Введите: /give_item [ID] [item_id]")
            self.bot.register_next_step_handler(msg, self.admin_give_item)
            
        elif call.data == "admin_give_energy":
            msg = self.bot.send_message(call.from_user.id, "⚡️ Введите: /give_energy [ID] [количество]")
            self.bot.register_next_step_handler(msg, self.admin_give_energy)
            
        elif call.data == "admin_give_premium":
            msg = self.bot.send_message(call.from_user.id, "⭐️ Введите: /give_premium [ID]")
            self.bot.register_next_step_handler(msg, self.admin_give_premium)
            
        elif call.data == "admin_stats":
            self.show_admin_stats(call.message)

    def admin_give_coins(self, message):
        if message.from_user.id not in ADMIN_IDS:
            return
        try:
            _, user_id, amount = message.text.split()
            user_id, amount = int(user_id), int(amount)
            self.db.add_coins(user_id, amount)
            self.bot.reply_to(message, f"✅ Выдано {amount} монет игроку {user_id}")
        except:
            self.bot.reply_to(message, "❌ Неверный формат команды!")

    def admin_give_item(self, message):
        if message.from_user.id not in ADMIN_IDS:
            return
        try:
            _, user_id, item_id = message.text.split()
            user_id, item_id = int(user_id), int(item_id)
            self.db.add_item_to_inventory(user_id, item_id)
            self.bot.reply_to(message, f"✅ Выдан предмет {item_id} игроку {user_id}")
        except:
            self.bot.reply_to(message, "❌ Неверный формат команды!")

    def show_admin_stats(self, message):
        total_users = self.db.get_total_users()
        total_coins = self.db.get_total_coins()
        premium_users = self.db.get_premium_users_count()
        
        stats = f"""
📊 Статистика бота:

👥 Всего игроков: {total_users}
💰 Всего монет: {total_coins}
⭐️ Премиум игроков: {premium_users}
"""
        self.bot.reply_to(message, stats)
