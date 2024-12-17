from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
from datetime import datetime

class ProfileHandler:
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db
        self.cooldowns = {}

    def handle_start(self, message):
        user_id = message.from_user.id
        username = message.from_user.username or "Анонимный"
        
        if not self.db.user_exists(user_id):
            self.db.create_user(user_id, username)
            welcome_text = (
                f"👋 Привет, {message.from_user.first_name}!\n\n"
                "🎮 Добро пожаловать в игру!\n"
                "🌟 Здесь ты можешь:\n"
                "💪 Тренироваться - /train\n"
                "⛏ Майнить - /mine\n"
                "🏃‍♂️ Смотреть профиль - /profile\n"
                "🎁 Открывать кейсы - /cases\n"
                "🏆 Смотреть топ игроков - /top\n"
                "🏭 Управлять фермой - /farm\n"
                "🎒 Инвентарь - /inventory\n"
                "🎫 Боевой пропуск - /battlepass\n"
                "📊 Статистика - /stats\n"
                "🎯 Достижения - /achievements\n"
                "🎲 Ежедневные награды - /daily\n"
                "❓ Помощь - /help"
            )
        else:
            welcome_text = (
                f"🎮 С возвращением, {message.from_user.first_name}!\n\n"
                "🌟 Доступные команды:\n"
                "💪 Тренироваться - /train\n"
                "⛏ Майнить - /mine\n"
                "🏃‍♂️ Профиль - /profile\n"
                "🎁 Кейсы - /cases\n"
                "🏆 Топ игроков - /top\n"
                "🏭 Ферма - /farm\n"
                "🎒 Инвентарь - /inventory\n"
                "🎫 Боевой пропуск - /battlepass\n"
                "📊 Статистика - /stats\n"
                "🎯 Достижения - /achievements\n"
                "🎲 Ежедневные награды - /daily\n"
                "❓ Помощь - /help"
            )
        
        self.bot.reply_to(message, welcome_text)

    def handle_profile(self, message):
        user_id = message.from_user.id
        user_data = self.db.get_user_data(user_id)
        battle_pass = self.db.get_battle_pass_data(user_id)
        
        profile_text = (
            f"👤 Профиль игрока {message.from_user.first_name}\n\n"
            f"🏆 Уровень: {user_data['level']}\n"
            f"⭐️ Опыт: {user_data['experience']}/1000\n"
            f"💰 Монеты: {user_data['coins']}\n"
            f"⚡️ Энергия: {user_data['energy']}/{user_data['energy_max']}\n"
            f"💪 Сила майнинга: {user_data['mining_power']}\n\n"
            f"🎫 Боевой пропуск:\n"
            f"└ 📊 Уровень: {battle_pass['level']}\n"
            f"└ ⭐️ Опыт: {battle_pass['exp']}/100\n"
            f"└ 👑 Премиум: {'Да' if battle_pass['is_premium'] else 'Нет'}\n\n"
            f"📊 Статистика:\n"
            f"└ 🏋️‍♂️ Всего тренировок: {user_data['total_trained']}\n"
            f"└ ⛏ Всего добыто: {user_data['total_mined']}\n"
            f"└ 📦 Открыто кейсов: {user_data.get('total_cases_opened', 0)}"
        )
        
        self.bot.reply_to(message, profile_text)

    def handle_top(self, message):
        top_users = self.db.get_top_users(10)
        
        top_text = "🏆 Топ 10 игроков:\n\n"
        for i, user in enumerate(top_users, 1):
            top_text += (
                f"{i}. {user['username']}\n"
                f"└ 🏆 Уровень: {user['level']}\n"
                f"└ 💰 Монеты: {user['coins']}\n"
                f"└ ⛏ Добыто: {user['total_mined']}\n"
            )
        
        self.bot.reply_to(message, top_text)

    def handle_stats(self, message):
        user_id = message.from_user.id
        stats = self.db.get_user_stats(user_id)
        
        stats_text = (
            f"📊 Статистика игрока {message.from_user.first_name}\n\n"
            f"💰 Всего заработано: {stats['total_coins_earned']}\n"
            f"💸 Всего потрачено: {stats['total_coins_spent']}\n"
            f"📦 Открыто кейсов: {stats['total_cases_opened']}\n"
            f"🎁 Получено предметов: {stats['total_items_obtained']}\n"
            f"🏆 Выполнено достижений: {stats['total_achievements_completed']}"
        )
        
        self.bot.reply_to(message, stats_text)

    def handle_help(self, message):
        help_text = (
            "❓ Помощь по командам:\n\n"
            "👤 Основные команды:\n"
            "└ /start - Начать игру\n"
            "└ /profile - Посмотреть профиль\n"
            "└ /top - Таблица лидеров\n"
            "└ /stats - Подробная статистика\n\n"
            "🎮 Игровые команды:\n"
            "└ /train - Тренироваться\n"
            "└ /mine - Майнить\n"
            "└ /farm - Управление фермой\n"
            "└ /cases - Открыть кейсы\n\n"
            "📦 Инвентарь и награды:\n"
            "└ /inventory - Открыть инвентарь\n"
            "└ /battlepass - Боевой пропуск\n"
            "└ /daily - Ежедневные награды\n"
            "└ /achievements - Достижения"
        )
        
        self.bot.reply_to(message, help_text)
