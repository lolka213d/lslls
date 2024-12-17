from telebot import types
import random

class MiningHandler:
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    def handle_mining(self, message):
        user = self.db.get_user_data(message.from_user.id)
        
        if user['energy'] < 1:
            return self.bot.reply_to(message, "⚡️ Недостаточно энергии для майнинга!")
            
        coins = random.randint(1, 5) * user['mining_power']
        exp = random.randint(10, 30)
        
        self.db.add_mining_reward(message.from_user.id, coins, exp)
        
        text = f"""
⛏ Вы намайнили:
💰 {coins} монет
✨ {exp} опыта
⚡️ -1 энергии

💪 Сила майнинга: {user['mining_power']}
"""
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("⛏ Майнить ещё", callback_data="mine_again"))
        
        self.bot.reply_to(message, text, reply_markup=markup)

    def handle_mining_callback(self, call):
        if call.data == "mine_again":
            user = self.db.get_user_data(call.from_user.id)
            
            if user['energy'] < 1:
                return self.bot.answer_callback_query(
                    call.id,
                    "⚡️ Недостаточно энергии!",
                    show_alert=True
                )
                
            coins = random.randint(1, 5) * user['mining_power']
            exp = random.randint(10, 30)
            
            self.db.add_mining_reward(call.from_user.id, coins, exp)
            
            text = f"""
⛏ Вы намайнили:
💰 {coins} монет
✨ {exp} опыта
⚡️ -1 энергии

💪 Сила майнинга: {user['mining_power']}
"""
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("⛏ Майнить ещё", callback_data="mine_again"))
            
            self.bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                reply_markup=markup
            )
