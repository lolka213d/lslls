from telebot import types
import random

class TrainingHandler:
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    def handle_training(self, message):
        user = self.db.get_user_data(message.from_user.id)
        
        if user['energy'] < 2:
            return self.bot.reply_to(message, "⚡️ Недостаточно энергии для тренировки!")
            
        exp = random.randint(20, 50)
        mining_power_up = random.random() < 0.3  # 30% шанс
        
        self.db.add_training_reward(message.from_user.id, exp, mining_power_up)
        
        text = f"""
🏋️‍♂️ Тренировка завершена!

✨ +{exp} опыта
⚡️ -2 энергии
"""
        if mining_power_up:
            text += "💪 Сила майнинга увеличена на 1!"
            
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🏋️‍♂️ Тренироваться ещё", callback_data="train_again"))
        
        self.bot.reply_to(message, text, reply_markup=markup)

    def handle_training_callback(self, call):
        if call.data == "train_again":
            user = self.db.get_user_data(call.from_user.id)
            
            if user['energy'] < 2:
                return self.bot.answer_callback_query(
                    call.id,
                    "⚡️ Недостаточно энергии!",
                    show_alert=True
                )
                
            exp = random.randint(20, 50)
            mining_power_up = random.random() < 0.3
            
            self.db.add_training_reward(call.from_user.id, exp, mining_power_up)
            
            text = f"""
🏋️‍♂️ Тренировка завершена!

✨ +{exp} опыта
⚡️ -2 энергии
"""
            if mining_power_up:
                text += "💪 Сила майнинга увеличена на 1!"
                
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("🏋️‍♂️ Тренироваться ещё", callback_data="train_again"))
            
            self.bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                reply_markup=markup
            )
