from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    user_id: int
    username: str
    dick_size: float = 0.0
    coins: int = 0
    energy: int = 5
    energy_max: int = 5
    mining_power: int = 1
    experience: int = 0
    level: int = 1
    battle_pass_exp: int = 0
    total_mined: int = 0
    total_trained: int = 0
    
    def can_mine(self):
        return self.energy > 0
        
    def can_level_up(self):
        return self.experience >= self.level * 100

@dataclass
class Farm:
    user_id: int
    level: int = 1
    production_rate: int = 1
    last_collection: datetime = datetime.now()
    
    def calculate_production(self):
        time_diff = (datetime.now() - self.last_collection).total_seconds()
        return int((time_diff / 3600) * self.production_rate * self.level)

@dataclass
class Case:
    id: int
    name: str
    price: int
    description: str
    rarity: str
    
    def get_rarity_multiplier(self):
        multipliers = {
            'common': 1,
            'rare': 2,
            'epic': 3,
            'legendary': 5
        }
        return multipliers.get(self.rarity.lower(), 1)

@dataclass
class Item:
    id: int
    name: str
    type: str
    description: str
    effect_value: float
    price: int
    
    def get_sell_price(self):
        return int(self.price * 0.7)

@dataclass
class BattlePass:
    id: int
    season: int
    price: int
    start_date: datetime
    end_date: datetime
    
    def is_active(self):
        now = datetime.now()
        return self.start_date <= now <= self.end_date

@dataclass
class Achievement:
    id: int
    name: str
    description: str
    requirement_type: str
    requirement_value: int
    reward_coins: int
    reward_exp: int
    
    def check_completion(self, current_value):
        return current_value >= self.requirement_value

@dataclass
class UserInventory:
    user_id: int
    item_id: int
    quantity: int
    
    def can_use(self, amount=1):
        return self.quantity >= amount
