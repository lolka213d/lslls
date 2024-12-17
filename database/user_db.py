from .base_db import BaseDatabase
from datetime import datetime

class UserDB(BaseDatabase):
    def get_user_data(self, user_id):
        return self.fetch_one(
            "SELECT * FROM users WHERE user_id = %s",
            (user_id,)
        )

    def create_user(self, user_id, username):
        self.execute_query(
            """
            INSERT INTO users (user_id, username, coins, energy, exp, level, 
            last_daily, daily_streak, created_at) 
            VALUES (%s, %s, 0, 100, 0, 1, NULL, 0, %s)
            """,
            (user_id, username, datetime.now())
        )

    def update_daily_reward(self, user_id, coins, energy, streak=1):
        self.execute_query(
            """
            UPDATE users 
            SET coins = coins + %s, 
                energy = energy + %s, 
                last_daily = %s,
                daily_streak = %s 
            WHERE user_id = %s
            """,
            (coins, energy, datetime.now(), streak, user_id)
        )

    def add_coins(self, user_id, amount):
        self.execute_query(
            "UPDATE users SET coins = coins + %s WHERE user_id = %s",
            (amount, user_id)
        )

    def add_energy(self, user_id, amount):
        self.execute_query(
            "UPDATE users SET energy = energy + %s WHERE user_id = %s",
            (amount, user_id)
        )

    def add_exp(self, user_id, amount):
        self.execute_query(
            "UPDATE users SET exp = exp + %s WHERE user_id = %s",
            (amount, user_id)
        )

    def get_top_users(self, limit=10):
        return self.fetch_all(
            "SELECT * FROM users ORDER BY level DESC, exp DESC LIMIT %s",
            (limit,)
        )
