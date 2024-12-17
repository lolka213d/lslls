from .base_db import BaseDatabase
from datetime import datetime

class InventoryDB(BaseDatabase):
    def get_user_inventory(self, user_id):
        return self.fetch_all(
            """
            SELECT i.*, it.name, it.description, it.type, it.rarity 
            FROM inventory i
            JOIN items it ON i.item_id = it.id
            WHERE i.user_id = %s
            """,
            (user_id,)
        )

    def add_item(self, user_id, item_id, amount=1):
        existing_item = self.fetch_one(
            "SELECT * FROM inventory WHERE user_id = %s AND item_id = %s",
            (user_id, item_id)
        )
        
        if existing_item:
            self.execute_query(
                """
                UPDATE inventory 
                SET amount = amount + %s 
                WHERE user_id = %s AND item_id = %s
                """,
                (amount, user_id, item_id)
            )
        else:
            self.execute_query(
                """
                INSERT INTO inventory (user_id, item_id, amount, obtained_at)
                VALUES (%s, %s, %s, %s)
                """,
                (user_id, item_id, amount, datetime.now())
            )

    def remove_item(self, user_id, item_id, amount=1):
        self.execute_query(
            """
            UPDATE inventory 
            SET amount = amount - %s 
            WHERE user_id = %s AND item_id = %s AND amount >= %s
            """,
            (amount, user_id, item_id, amount)
        )
        
        # Clean up items with 0 amount
        self.execute_query(
            "DELETE FROM inventory WHERE amount <= 0"
        )

    def get_item_count(self, user_id, item_id):
        result = self.fetch_one(
            "SELECT amount FROM inventory WHERE user_id = %s AND item_id = %s",
            (user_id, item_id)
        )
        return result['amount'] if result else 0
