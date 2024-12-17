from .base_db import BaseDatabase
from datetime import datetime

class FarmDB(BaseDatabase):
    def get_farm_data(self, user_id):
        return self.fetch_one(
            "SELECT * FROM farms WHERE user_id = %s",
            (user_id,)
        )

    def create_farm(self, user_id):
        self.execute_query(
            """
            INSERT INTO farms (user_id, level, exp, last_harvest, crops)
            VALUES (%s, 1, 0, NULL, 0)
            """,
            (user_id,)
        )

    def plant_crops(self, user_id, amount):
        self.execute_query(
            """
            UPDATE farms 
            SET crops = crops + %s,
                last_harvest = %s
            WHERE user_id = %s
            """,
            (amount, datetime.now(), user_id)
        )

    def harvest_crops(self, user_id):
        farm_data = self.get_farm_data(user_id)
        if farm_data:
            coins_earned = farm_data['crops'] * farm_data['level']
            exp_earned = farm_data['crops'] * 2

            self.execute_query(
                """
                UPDATE farms 
                SET crops = 0,
                    exp = exp + %s
                WHERE user_id = %s
                """,
                (exp_earned, user_id)
            )

            self.execute_query(
                "UPDATE users SET coins = coins + %s WHERE user_id = %s",
                (coins_earned, user_id)
            )

            return coins_earned, exp_earned
        return 0, 0

    def level_up_farm(self, user_id):
        self.execute_query(
            """
            UPDATE farms 
            SET level = level + 1,
                exp = 0
            WHERE user_id = %s
            """,
            (user_id,)
        )
