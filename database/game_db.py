from .base_db import BaseDatabase
from datetime import datetime

class GameDB(BaseDatabase):
    def get_game_stats(self, user_id):
        return self.fetch_one(
            """
            SELECT 
                games_played,
                games_won,
                total_rewards,
                highest_score
            FROM game_stats 
            WHERE user_id = %s
            """,
            (user_id,)
        )

    def create_game_stats(self, user_id):
        self.execute_query(
            """
            INSERT INTO game_stats 
            (user_id, games_played, games_won, total_rewards, highest_score)
            VALUES (%s, 0, 0, 0, 0)
            """,
            (user_id,)
        )

    def record_game_result(self, user_id, won, score, reward):
        self.execute_query(
            """
            UPDATE game_stats 
            SET games_played = games_played + 1,
                games_won = games_won + %s,
                total_rewards = total_rewards + %s,
                highest_score = GREATEST(highest_score, %s)
            WHERE user_id = %s
            """,
            (1 if won else 0, reward, score, user_id)
        )

    def get_leaderboard(self, limit=10):
        return self.fetch_all(
            """
            SELECT u.username, gs.* 
            FROM game_stats gs
            JOIN users u ON gs.user_id = u.user_id
            ORDER BY gs.highest_score DESC
            LIMIT %s
            """,
            (limit,)
        )
