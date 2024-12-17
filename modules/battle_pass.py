from telebot import types
from config.config import PAYMENT_TOKEN
from datetime import datetime
import random

class BattlePass:
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    def show_battle_pass(self, user_id):
        bp_data = self.db.get_battle_pass_data(user_id)
        if not bp_data:
            self.db.create_battle_pass_user(user_id)
            bp_data = self.db.get_battle_pass_data(user_id)

        text = self.generate_battle_pass_text(bp_data)
        markup = self.generate_battle_pass_markup(bp_data['is_premium'])
        return text, markup

    def generate_battle_pass_text(self, bp_data):
        return f"""
⭐ Боевой Пропуск (Сезон {bp_data['season']})

📊 Уровень: {bp_data['level']}
✨ Опыт: {bp_data['exp']}/1000
🎖 Статус: {'Премиум' if bp_data['is_premium'] else 'Бесплатный'}
"""

    def generate_battle_pass_markup(self, is_premium):
        markup = types.InlineKeyboardMarkup(row_width=2)
        if not is_premium:
            markup.add(types.InlineKeyboardButton("💎 Купить Премиум", callback_data="premium_pass"))
        
        markup.add(
            types.InlineKeyboardButton("🎁 Награды", callback_data="pass_rewards"),
            types.InlineKeyboardButton("📦 Собрать награды", callback_data="collect_rewards")
        )
        return markup

    def refresh_battle_pass_message(self, user_id, message_id):
        bp_data = self.db.get_battle_pass_data(user_id)
        text = self.generate_battle_pass_text(bp_data)
        markup = self.generate_battle_pass_markup(bp_data['is_premium'])

        try:
            self.bot.edit_message_text(
                text,
                chat_id=user_id,
                message_id=message_id,
                reply_markup=markup
            )
        except:
            pass  # Message is identical

    def show_rewards(self, user_id):
        bp_data = self.db.get_battle_pass_data(user_id)
        rewards = self.db.get_battle_pass_rewards(bp_data['level'], bp_data['is_premium'])

        text = "🎁 Награды текущего уровня:\n\n"
        if bp_data['level'] == 1:
            text += "На 1 уровне наград нет. Играйте чтобы получить награды!\n"
        else:
            for reward in rewards:
                text += f"{'💎' if reward['is_premium'] else '🎁'} {reward['description']}\n"

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("◀️ Назад", callback_data="back_to_pass"))
        return text, markup

    def collect_rewards(self, user_id):
        bp_data = self.db.get_battle_pass_data(user_id)
        rewards = self.db.get_battle_pass_rewards(bp_data['level'], bp_data['is_premium'])
        
        if bp_data['level'] == 1:
            return "На 1 уровне наград нет. Играйте чтобы получить награды!"
            
        collected = []
        for reward in rewards:
            if reward['type'] == 'coins':
                amount = random.randint(5, 30)
                self.db.add_coins(user_id, amount)
                collected.append(f"💰 +{amount} монет")
            elif reward['type'] == 'item':
                self.db.add_item_to_inventory(user_id, reward['item_id'])
                collected.append(f"📦 {reward['description']}")
                
        if collected:
            self.db.mark_rewards_collected(user_id, bp_data['level'])
            return "🎁 Собранные награды:\n" + "\n".join(collected)
        else:
            return "❌ Награды уже собраны или недоступны"

    def handle_premium_purchase(self, call):
        prices = [
            {
                "label": "Премиум Боевой Пропуск",
                "amount": 29900  # 299.00 RUB
            }
        ]
        
        self.bot.send_invoice(
            chat_id=call.message.chat.id,
            title="Премиум Боевой Пропуск",
            description="Разблокируйте премиум награды в боевом пропуске!",
            provider_token=PAYMENT_TOKEN,
            currency="RUB",
            prices=prices,
            start_parameter="premium_pass",
            invoice_payload="premium_pass"
        )

    def process_premium_purchase(self, payment):
        if payment.invoice_payload == "premium_pass":
            user_id = payment.chat.id
            self.db.upgrade_battle_pass(user_id)
            self.bot.send_message(user_id, "🎉 Поздравляем! Вы приобрели Премиум Боевой Пропуск!")

    def add_experience(self, user_id, exp):
        old_level = self.db.get_battle_pass_data(user_id)['level']
        self.db.add_battle_pass_exp(user_id, exp)
        new_data = self.db.get_battle_pass_data(user_id)
        
        if new_data['level'] > old_level:
            rewards = self.db.get_battle_pass_rewards(new_data['level'], new_data['is_premium'])
            reward_text = f"🎉 Новый уровень в Боевом Пропуске! ({new_data['level']})\n\nДоступные награды:\n"
            for reward in rewards:
                reward_text += f"{'💎' if reward['is_premium'] else '🎁'} {reward['description']}\n"
            
            self.bot.send_message(user_id, reward_text)

    def handle_callback(self, call):
        user_id = call.message.chat.id
        message_id = call.message.message_id

        if call.data == "premium_pass":
            self.handle_premium_purchase(call)
            self.refresh_battle_pass_message(user_id, message_id)
            
        elif call.data == "pass_rewards":
            text, markup = self.show_rewards(user_id)
            self.bot.edit_message_text(
                text,
                chat_id=user_id,
                message_id=message_id,
                reply_markup=markup
            )
            
        elif call.data == "collect_rewards":
            text = self.collect_rewards(user_id)
            self.bot.answer_callback_query(call.id, text, show_alert=True)
            self.refresh_battle_pass_message(user_id, message_id)
            
        elif call.data == "back_to_pass":
            text, markup = self.show_battle_pass(user_id)
            self.bot.edit_message_text(
                text,
                chat_id=user_id,
                message_id=message_id,
                reply_markup=markup
            )
