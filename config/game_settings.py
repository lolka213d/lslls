# Game Settings
DAILY_REWARD_MIN = 50
DAILY_REWARD_MAX = 100
EXP_PER_LEVEL = 1000
MINING_BASE_REWARD = (5, 15)
TRAINING_EXP_RANGE = (10, 30)
TRAINING_COINS_RANGE = (5, 15)

# Starting Values
STARTING_COINS = 100
STARTING_ENERGY = 10
STARTING_ENERGY_MAX = 10
STARTING_MINING_POWER = 1
STARTING_LEVEL = 1

# Shop Prices
PRICES = {
    'energy_1': 50,
    'energy_5': 200,
    'mining_upgrade': 300,
    'energy_max_upgrade': 500
}

# Farm Settings
FARM_BASE_PRODUCTION = 10
FARM_UPGRADE_COST = 1000
FARM_PRODUCTION_MULTIPLIER = 1.5
FARM_COLLECTION_COOLDOWN = 3600  # in seconds
FARM_MAX_LEVEL = 10

# Battle Pass
BATTLE_PASS_PRICE = 299
BATTLE_PASS_LEVELS = 100
BATTLE_PASS_EXP_PER_LEVEL = 1000
BATTLE_PASS_SEASON_DURATION = 30  # in days

# Cases Settings
CASES = {
    'common': {
        'price': 100,
        'rewards': {
            'coins': (50, 200),
            'energy': (1, 3),
            'exp': (50, 150)
        }
    },
    'rare': {
        'price': 300,
        'rewards': {
            'coins': (200, 500),
            'energy': (3, 7),
            'exp': (150, 300)
        }
    },
    'epic': {
        'price': 1000,
        'rewards': {
            'coins': (500, 2000),
            'energy': (7, 15),
            'exp': (300, 1000)
        }
    }
}

# Level Up Rewards
LEVEL_UP_REWARDS = {
    'coins': 100,
    'energy': 5
}

# Cooldowns (in seconds)
COOLDOWNS = {
    'train': 300,
    'mine': 300,
    'daily': 86400
}
