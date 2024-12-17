from datetime import datetime
import random
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

class DailyHandler:
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    def handle_daily(self, message):
        user_id = message.from_user.id
        user = self.db.get_user_data(user_id)
        now = datetime.now()
        
        if not user['last_daily'] or (now - user['last_daily']).days >= 1:
            # Base rewards
            coins = random.randint(100, 500)
            energy = random.randint(5, 15)
            
            # Bonus for streak
            streak = user.get('daily_streak', 0) + 1
            bonus_coins = streak * 50
            bonus_energy = streak * 2
            
            total_coins = coins + bonus_coins
            total_energy = energy + bonus_energy
            
            self.db.update_daily_reward(user_id, total_coins, total_energy, streak)
            
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("🎁 Открыть бонусный кейс", callback_data="daily:bonus_case"))
            
            text = (
                "🎁 Ежедневная награда получена!\n\n"
                f"Получено:\n"
                f"💰 {total_coins} монет (+ {bonus_coins} за серию)\n"
                f"⚡️ {total_energy} энергии (+ {bonus_energy} за серию)\n"
                f"🔥 Серия: {streak} дней"
            )
            
            self.bot.reply_to(message, text, reply_markup=markup)
        else:
            hours_left = 24 - (now - user['last_daily']).seconds // 3600
            minutes_left = 60 - ((now - user['last_daily']).seconds % 3600) // 60
            
            text = (
                f"⏳ До следующей награды:\n"
                f"└ {hours_left} ч. {minutes_left} мин.\n"
                f"🔥 Текущая серия: {user.get('daily_streak', 0)} дней"
            )
            
            self.bot.reply_to(message, text)

    def handle_callback(self, call):
        if call.data == "daily:bonus_case":
            user_id = call.from_user.id
            reward = random.choice(['coins', 'energy', 'exp'])
            amount = random.randint(50, 200)
            
            if reward == 'coins':
                self.db.add_coins(user_id, amount)
                text = f"🎁 Из бонусного кейса выпало:\n└ 💰 {amount} монет"
            elif reward == 'energy':
                self.db.add_energy(user_id, amount)
                text = f"🎁 Из бонусного кейса выпало:\n└ ⚡️ {amount} энергии"
            else:
                self.db.add_exp(user_id, amount)
                text = f"🎁 Из бонусного кейса выпало:\n└ ⭐️ {amount} опыта"
            
            self.bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id
            )
