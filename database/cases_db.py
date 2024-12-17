from .base_db import BaseDatabase
from datetime import datetime

class CasesDB(BaseDatabase):
    def get_user_cases(self, user_id):
        return self.fetch_all(
            "SELECT * FROM user_cases WHERE user_id = %s",
            (user_id,)
        )

    def get_case_info(self, case_id):
        return self.fetch_one(
            "SELECT * FROM cases WHERE id = %s",
            (case_id,)
        )

    def add_case_to_user(self, user_id, case_id):
        self.execute_query(
            """
            INSERT INTO user_cases (user_id, case_id, obtained_at)
            VALUES (%s, %s, %s)
            """,
            (user_id, case_id, datetime.now())
        )

    def open_case(self, user_id, case_id):
        # Remove case from inventory
        self.execute_query(
            "DELETE FROM user_cases WHERE user_id = %s AND case_id = %s LIMIT 1",
            (user_id, case_id)
        )

    def get_available_cases(self):
        return self.fetch_all(
            "SELECT * FROM cases WHERE is_available = 1"
        )

    def record_case_reward(self, user_id, case_id, reward_type, reward_amount):
        self.execute_query(
            """
            INSERT INTO case_history (user_id, case_id, reward_type, reward_amount, opened_at)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (user_id, case_id, reward_type, reward_amount, datetime.now())
        )
