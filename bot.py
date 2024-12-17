import telebot
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging
import time
from datetime import datetime
from config.config import BOT_TOKEN as TOKEN

from modules.handlers import (
    ProfileHandler, 
    MiningHandler, 
    TrainingHandler, 
    CaseHandler,
    FarmHandler,
    InventoryHandler,
    BattlePassHandler,
    AchievementsHandler,
    ShopHandler,
    DailyHandler,
    AdminHandler,
    QuestHandler
)

from database import Database


class States(StatesGroup):
    waiting_for_shop_choice = State()
    waiting_for_item_amount = State()
    waiting_for_confirmation = State()

class Bot:
    def __init__(self):
        state_storage = StateMemoryStorage()
        self.bot = telebot.TeleBot(TOKEN, state_storage=state_storage)
        self.db = Database()
        self.setup_handlers()
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('bot.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def setup_handlers(self):
        self.handler = {
            'profile': ProfileHandler(self.bot, self.db),
            'mining': MiningHandler(self.bot, self.db),
            'training': TrainingHandler(self.bot, self.db),
            'cases': CaseHandler(self.bot, self.db),
            'farm': FarmHandler(self.bot, self.db),
            'inventory': InventoryHandler(self.bot, self.db),
            'battlepass': BattlePassHandler(self.bot, self.db),
            'achievements': AchievementsHandler(self.bot, self.db),
            'shop': ShopHandler(self.bot, self.db),
            'daily': DailyHandler(self.bot, self.db),
            'quest': QuestHandler(self.bot, self.db)
        }

        # Основные команды
        @self.bot.message_handler(commands=['start'])
        def start(message):
            try:
                self.handler['profile'].handle_start(message)
            except Exception as e:
                self.logger.error(f"Error in start handler: {e}")
                self.bot.reply_to(message, "Произошла ошибка. Попробуйте позже.")

        @self.bot.message_handler(commands=['profile'])
        def profile(message):
            try:
                self.handler['profile'].handle_profile(message)
            except Exception as e:
                self.logger.error(f"Error in profile handler: {e}")
                self.bot.reply_to(message, "Произошла ошибка. Попробуйте позже.")

        @self.bot.message_handler(commands=['top'])
        def top(message):
            try:
                self.handler['profile'].handle_top(message)
            except Exception as e:
                self.logger.error(f"Error in top handler: {e}")
                self.bot.reply_to(message, "Произошла ошибка. Попробуйте позже.")

        # Игровые команды
        @self.bot.message_handler(commands=['mine'])
        def mine(message):
            try:
                self.handler['mining'].handle_mining(message)
            except Exception as e:
                self.logger.error(f"Error in mining handler: {e}")
                self.bot.reply_to(message, "Произошла ошибка. Попробуйте позже.")

        @self.bot.message_handler(commands=['train'])
        def train(message):
            try:
                self.handler['training'].handle_training(message)
            except Exception as e:
                self.logger.error(f"Error in training handler: {e}")
                self.bot.reply_to(message, "Произошла ошибка. Попробуйте позже.")

        @self.bot.message_handler(commands=['cases'])
        def cases(message):
            try:
                self.handler['cases'].handle_cases(message)
            except Exception as e:
                self.logger.error(f"Error in cases handler: {e}")
                self.bot.reply_to(message, "Произошла ошибка. Попробуйте позже.")

        @self.bot.message_handler(commands=['farm'])
        def farm(message):
            try:
                self.handler['farm'].handle_farm(message)
            except Exception as e:
                self.logger.error(f"Error in farm handler: {e}")
                self.bot.reply_to(message, "Произошла ошибка. Попробуйте позже.")

        @self.bot.message_handler(commands=['shop'])
        def shop(message):
            try:
                self.handler['shop'].handle_shop(message)
            except Exception as e:
                self.logger.error(f"Error in shop handler: {e}")
                self.bot.reply_to(message, "Произошла ошибка. Попробуйте позже.")

        @self.bot.message_handler(commands=['daily'])
        def daily(message):
            try:
                self.handler['daily'].handle_daily(message)
            except Exception as e:
                self.logger.error(f"Error in daily handler: {e}")
                self.bot.reply_to(message, "Произошла ошибка. Попробуйте позже.")

        @self.bot.message_handler(commands=['quest'])
        def quest(message):
            try:
                self.handler['quest'].handle_quest(message)
            except Exception as e:
                self.logger.error(f"Error in quest handler: {e}")
                self.bot.reply_to(message, "Произошла ошибка. Попробуйте позже.")

        # Колбэки
        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_handler(call):
            try:
                action = call.data.split(':')[0]
                if action in self.handler:
                    self.handler[action].handle_callback(call)
                else:
                    self.logger.warning(f"Unknown callback action: {action}")
            except Exception as e:
                self.logger.error(f"Error in callback handler: {e}")
                self.bot.answer_callback_query(call.id, "Произошла ошибка. Попробуйте позже.")

    def run(self):
        self.logger.info("🚀 Бот запущен!")
        try:
            self.bot.polling(none_stop=True, interval=0)
        except Exception as e:
            self.logger.error(f"❌ Критическая ошибка: {e}")
            raise e

    def stop(self):
        self.logger.info("🛑 Бот остановлен")
        self.bot.stop_polling()
