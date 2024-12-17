from .base_db import BaseDatabase
from datetime import datetime

class MiningDB(BaseDatabase):
    def get_mining_data(self, user_id):
        return self.fetch_one(
            "SELECT * FROM mining WHERE user_id = %s",
            (user_id,)
        )

    def create_mining_data(self, user_id):
        self.execute_query(
            """
            INSERT INTO mining (user_id, last_mining, mining_level, mining_exp)
            VALUES (%s, NULL, 1, 0)
            """,
            (user_id,)
        )

    def update_mining(self, user_id, coins_earned, exp_earned):
        self.execute_query(
            """
            UPDATE mining 
            SET last_mining = %s,
                mining_exp = mining_exp + %s
            WHERE user_id = %s
            """,
            (datetime.now(), exp_earned, user_id)
        )
        
        self.execute_query(
            "UPDATE users SET coins = coins + %s WHERE user_id = %s",
            (coins_earned, user_id)
        )

    def level_up_mining(self, user_id):
        self.execute_query(
            """
            UPDATE mining 
            SET mining_level = mining_level + 1,
                mining_exp = 0
            WHERE user_id = %s
            """,
            (user_id,)
        )
