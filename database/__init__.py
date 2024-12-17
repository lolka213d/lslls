from .base_db import BaseDatabase
from .user_db import UserDB
from .mining_db import MiningDB
from .training_db import TrainingDB
from .cases_db import CasesDB
from .farm_db import FarmDB
from .inventory_db import InventoryDB
from .game_db import GameDB
from .models import User, Farm, Case, Item, BattlePass, Achievement, UserInventory

class Database:
    def __init__(self):
        self.base = BaseDatabase()
        self.user = UserDB()
        self.mining = MiningDB()
        self.training = TrainingDB()
        self.cases = CasesDB()
        self.farm = FarmDB()
        self.inventory = InventoryDB()
        self.game = GameDB()

    def __del__(self):
        if hasattr(self, 'base'):
            del self.base

__all__ = [
    'Database',
    'User',
    'Farm',
    'Case',
    'Item',
    'BattlePass',
    'Achievement',
    'UserInventory'
]
