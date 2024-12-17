from .base_db import BaseDatabase
from datetime import datetime

class TrainingDB(BaseDatabase):
    def get_training_data(self, user_id):
        return self.fetch_one(
            "SELECT * FROM training WHERE user_id = %s",
            (user_id,)
        )

    def create_training_data(self, user_id):
        self.execute_query(
            """
            INSERT INTO training (user_id, last_training, training_level, training_exp)
            VALUES (%s, NULL, 1, 0)
            """,
            (user_id,)
        )

    def update_training(self, user_id, energy_spent, exp_earned):
        self.execute_query(
            """
            UPDATE training 
            SET last_training = %s,
                training_exp = training_exp + %s
            WHERE user_id = %s
            """,
            (datetime.now(), exp_earned, user_id)
        )
        
        self.execute_query(
            "UPDATE users SET energy = energy - %s WHERE user_id = %s",
            (energy_spent, user_id)
        )

    def level_up_training(self, user_id):
        self.execute_query(
            """
            UPDATE training 
            SET training_level = training_level + 1,
                training_exp = 0
            WHERE user_id = %s
            """,
            (user_id,)
        )
