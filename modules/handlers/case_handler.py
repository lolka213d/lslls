from telebot import types
import random
from config.game_settings import CASES

class CaseHandler:
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    def handle_cases(self, message):
        markup = types.InlineKeyboardMarkup(row_width=2)
        for case_name, case_data in CASES.items():
            markup.add(types.InlineKeyboardButton(
                f"📦 {case_name.title()} кейс ({case_data['price']} монет)",
                callback_data=f"open_case_{case_name}"
            ))
        
        self.bot.reply_to(message, "📦 Доступные кейсы:", reply_markup=markup)

    def handle_case_callback(self, call):
        if "open_case" in call.data:
            case_name = call.data.split('_')[-1]
            case_data = CASES[case_name]
            user = self.db.get_user_data(call.from_user.id)
            
            if user['coins'] >= case_data['price']:
                rewards = self.open_case(case_name)
                self.db.spend_coins(call.from_user.id, case_data['price'])
                self.apply_rewards(call.from_user.id, rewards)
                
                reward_text = "\n".join([f"{k}: {v}" for k, v in rewards.items()])
                self.bot.edit_message_text(
                    f"📦 Кейс открыт!\n\nНаграды:\n{reward_text}",
                    call.message.chat.id,
                    call.message.message_id
                )
            else:
                self.bot.answer_callback_query(
                    call.id,
                    "💰 Недостаточно монет для открытия кейса!",
                    show_alert=True
                )

    def open_case(self, case_name):
        case = CASES[case_name]
        rewards = {}
        
        for reward_type, chance in case['rewards'].items():
            if random.random() < chance:
                if reward_type == 'coins':
                    rewards['coins'] = random.randint(case['min_coins'], case['max_coins'])
                elif reward_type == 'energy':
                    rewards['energy'] = random.randint(3, 10)
                elif reward_type == 'exp':
                    rewards['exp'] = random.randint(50, 200)
                elif reward_type == 'items':
                    item_id = random.choice(case['possible_items'])
                    rewards['item'] = item_id
        
        return rewards

    def apply_rewards(self, user_id, rewards):
        for reward_type, amount in rewards.items():
            if reward_type == 'coins':
                self.db.add_coins(user_id, amount)
            elif reward_type == 'energy':
                self.db.add_energy(user_id, amount)
            elif reward_type == 'exp':
                self.db.add_experience(user_id, amount)
            elif reward_type == 'item':
                self.db.add_item_to_inventory(user_id, amount)
