from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config.config import CRYPTO_BOT_TOKEN, PAYMENT_TOKEN

class BattlePassHandler:
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db
        self.crypto_token = CRYPTO_BOT_TOKEN
        self.payment_token = PAYMENT_TOKEN

    def handle_battlepass(self, message):
        user_id = message.from_user.id
        bp_data = self.db.get_battlepass_data(user_id)
        
        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton("🎯 Награды", callback_data="battlepass:rewards"),
            InlineKeyboardButton("💎 Премиум", callback_data="battlepass:premium")
        )
        
        text = (
            f"🎫 Боевой пропуск\n\n"
            f"📊 Уровень: {bp_data['level']}\n"
            f"⭐️ Опыт: {bp_data['exp']}/100\n"
            f"👑 Премиум: {'Да' if bp_data['is_premium'] else 'Нет'}\n\n"
            f"🎁 Доступные награды: {bp_data['available_rewards']}"
        )
        
        self.bot.reply_to(message, text, reply_markup=markup)

    def handle_premium_purchase(self, call):
        user_id = call.from_user.id
        
        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton("💳 CryptoBot", callback_data="payment:crypto"),
            InlineKeyboardButton("💰 Smart Glocal", callback_data="payment:smart")
        )
        markup.row(InlineKeyboardButton("↩️ Назад", callback_data="battlepass:rewards"))
        
        text = (
            "💎 Премиум боевой пропуск\n\n"
            "💵 Стоимость: $5\n"
            "✨ Преимущества:\n"
            "└ Дополнительные награды\n"
            "└ x2 опыта\n"
            "└ Эксклюзивные предметы\n"
            "└ Особый статус\n\n"
            "💳 Выберите способ оплаты:"
        )
        
        self.bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    def handle_payment(self, call):
        user_id = call.from_user.id
        payment_type = call.data.split(':')[1]
        amount = 5  # USD

        if payment_type == 'crypto':
            payload = f"battlepass_premium_{user_id}"
            payment_url = f"https://t.me/CryptoBot?start=pay_{self.crypto_token}_{amount}_{payload}"
        else:  # Smart Glocal
            payment_url = f"https://pay.smart-glocal.com/payment/{self.payment_token}?amount={amount}&user_id={user_id}"

        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton("💎 Оплатить", url=payment_url),
            InlineKeyboardButton("↩️ Назад", callback_data="battlepass:premium")
        )
        
        self.bot.edit_message_text(
            "🔒 Перейдите по ссылке для оплаты.\nПосле успешной оплаты премиум будет активирован автоматически!",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    def handle_callback(self, call):
        action = call.data.split(':')[1]
        
        if action == 'premium':
            self.handle_premium_purchase(call)
        elif action.startswith('payment'):
            self.handle_payment(call)
        elif action == 'rewards':
            rewards = self.db.get_battlepass_rewards(call.from_user.id)
            text = "🎁 Награды боевого пропуска:\n\n"
            for reward in rewards:
                status = "✅" if reward['claimed'] else "❌"
                text += f"{status} Уровень {reward['level']}: {reward['description']}\n"
            
            self.bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                reply_markup=call.message.reply_markup
            )
