from telebot import types

def get_shop_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🎁 Кейсы", callback_data="shop_cases"),
        types.InlineKeyboardButton("🏭 Улучшения фермы", callback_data="shop_farm")
    )
    markup.add(types.InlineKeyboardButton("⭐ Боевой пропуск", callback_data="shop_battlepass"))
    return markup

def get_case_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("📦 Обычный кейс - 100💰", callback_data="case_1"),
        types.InlineKeyboardButton("📦 Редкий кейс - 250💰", callback_data="case_2"),
        types.InlineKeyboardButton("📦 Эпический кейс - 500💰", callback_data="case_3"),
        types.InlineKeyboardButton("📦 Легендарный кейс - 1000💰", callback_data="case_4")
    )
    return markup

def get_battle_pass_keyboard(is_premium=False):
    markup = types.InlineKeyboardMarkup(row_width=2)
    if not is_premium:
        markup.add(types.InlineKeyboardButton("🌟 Купить Премиум", callback_data="premium_pass"))
    markup.add(
        types.InlineKeyboardButton("📜 Награды", callback_data="pass_rewards"),
        types.InlineKeyboardButton("📊 Прогресс", callback_data="pass_progress")
    )
    return markup

def get_farm_keyboard(farm_level):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("⚡ Собрать", callback_data="farm_collect"),
        types.InlineKeyboardButton("⬆️ Улучшить", callback_data="farm_upgrade")
    )
    return markup
