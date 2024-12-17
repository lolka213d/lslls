from telebot import types
from datetime import datetime, timedelta

class FarmHandler:
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    def handle_farm(self, message):
        farm = self.db.get_farm_data(message.from_user.id)
        now = datetime.now()
        last_collection = farm['last_collection']
        hours_passed = (now - last_collection).total_seconds() / 3600
        coins_produced = int(farm['production_rate'] * hours_passed)
        
        text = f"""
🌾 Ваша ферма

📊 Уровень: {farm['level']}
⚡️ Производство: {farm['production_rate']} монет/час
💰 Накоплено: {coins_produced} монет
⏳ Последний сбор: {last_collection.strftime('%d.%m.%Y %H:%M')}
"""
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("💰 Собрать", callback_data="collect_farm"),
            types.InlineKeyboardButton("⬆️ Улучшить", callback_data="upgrade_farm")
        )
        
        self.bot.reply_to(message, text, reply_markup=markup)

    def handle_farm_callback(self, call):
        if call.data == "collect_farm":
            farm = self.db.get_farm_data(call.from_user.id)
            now = datetime.now()
            hours_passed = (now - farm['last_collection']).total_seconds() / 3600
            coins_produced = int(farm['production_rate'] * hours_passed)
            
            if coins_produced > 0:
                self.db.collect_farm(call.from_user.id, coins_produced)
                self.bot.answer_callback_query(
                    call.id,
                    f"✅ Собрано {coins_produced} монет!",
                    show_alert=True
                )
            else:
                self.bot.answer_callback_query(
                    call.id,
                    "⏳ Пока нечего собирать!",
                    show_alert=True
                )
                
        elif call.data == "upgrade_farm":
            farm = self.db.get_farm_data(call.from_user.id)
            upgrade_cost = farm['level'] * 1000
            
            if self.db.get_user_coins(call.from_user.id) >= upgrade_cost:
                self.db.upgrade_farm(call.from_user.id, upgrade_cost)
                self.bot.answer_callback_query(
                    call.id,
                    f"✅ Ферма улучшена до уровня {farm['level'] + 1}!",
                    show_alert=True
                )
            else:
                self.bot.answer_callback_query(
                    call.id,
                    f"💰 Недостаточно монет! Нужно: {upgrade_cost}",
                    show_alert=True
                )
