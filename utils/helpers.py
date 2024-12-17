from datetime import datetime, timedelta
from config.constants import *

def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{int(hours)}ч {int(minutes)}м {int(seconds)}с"

def calculate_level(exp):
    return (exp // EXP_PER_LEVEL) + 1

def format_number(number):
    if number < 1000:
        return str(number)
    elif number < 1000000:
        return f"{number/1000:.1f}K"
    else:
        return f"{number/1000000:.1f}M"

def get_reward_multiplier(is_premium, has_booster):
    multiplier = 1.0
    if is_premium:
        multiplier *= PREMIUM_MULTIPLIER
    if has_booster:
        multiplier *= BOOSTER_MULTIPLIER
    return multiplier

def calculate_farm_income(last_collection, production_rate):
    time_passed = (datetime.now() - last_collection).total_seconds()
    hours = time_passed / 3600
    return int(hours * production_rate)

def get_next_level_exp(current_level):
    return current_level * EXP_PER_LEVEL
