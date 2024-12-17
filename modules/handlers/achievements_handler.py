from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

class AchievementsHandler:
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    def handle_achievements(self, message):
        user_id = message.from_user.id
        achievements = self.db.get_user_achievements(user_id)
        
        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton("🎯 Обычные", callback_data="achievements:normal"),
            InlineKeyboardButton("🌟 Редкие", callback_data="achievements:rare")
        )
        markup.row(
            InlineKeyboardButton("👑 Легендарные", callback_data="achievements:legendary")
        )
        
        text = "🏆 Ваши достижения:\n\n"
        for ach in achievements:
            status = "✅" if ach['completed'] else "❌"
            text += f"{status} {ach['name']} - {ach['description']}\n"
        
        self.bot.reply_to(message, text, reply_markup=markup)

    def handle_callback(self, call):
        user_id = call.from_user.id
        action = call.data.split(':')[1]
        
        achievements = self.db.get_achievements_by_type(user_id, action)
        text = f"🏆 {action.title()} достижения:\n\n"
        
        for ach in achievements:
            status = "✅" if ach['completed'] else "❌"
            text += f"{status} {ach['name']} - {ach['description']}\n"
            if ach['completed']:
                text += f"└ Награда: {ach['reward']} 💰\n"
        
        self.bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=call.message.reply_markup
        )
