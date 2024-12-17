from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

class QuestHandler:
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    def handle_quests(self, message):
        user_id = message.from_user.id
        quests = self.db.get_user_quests(user_id)
        
        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton("🎯 Ежедневные", callback_data="quest:daily"),
            InlineKeyboardButton("📜 Еженедельные", callback_data="quest:weekly")
        )
        
        text = "📋 Ваши задания:\n\n"
        for quest in quests:
            status = "✅" if quest['completed'] else "⏳"
            progress = f"({quest['progress']}/{quest['target']})"
            text += f"{status} {quest['name']} {progress}\n"
            text += f"└ Награда: {quest['reward']} 💰\n"
        
        self.bot.reply_to(message, text, reply_markup=markup)

    def handle_callback(self, call):
        quest_type = call.data.split(':')[1]
        user_id = call.from_user.id
        
        quests = self.db.get_quests_by_type(user_id, quest_type)
        text = f"📋 {quest_type.title()} задания:\n\n"
        
        for quest in quests:
            status = "✅" if quest['completed'] else "⏳"
            progress = f"({quest['progress']}/{quest['target']})"
            text += f"{status} {quest['name']} {progress}\n"
            text += f"└ Награда: {quest['reward']} 💰\n"
        
        self.bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=call.message.reply_markup
        )
