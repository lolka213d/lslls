import mysql.connector
from datetime import datetime
from config.config import DB_CONFIG

class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(**DB_CONFIG)
        self.cursor = self.connection.cursor(dictionary=True)
        self.create_tables()

    def create_tables(self):
        # Users table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id BIGINT PRIMARY KEY,
                username VARCHAR(255),
                coins INT DEFAULT 100,
                level INT DEFAULT 1,
                experience INT DEFAULT 0,
                energy INT DEFAULT 10,
                energy_max INT DEFAULT 10,
                mining_power INT DEFAULT 1,
                total_mined INT DEFAULT 0,
                total_trained INT DEFAULT 0,
                last_daily DATETIME,
                registration_date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Inventory table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id BIGINT,
                item_id INT,
                quantity INT DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        # Battle Pass table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS battle_pass (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id BIGINT,
                level INT DEFAULT 1,
                exp INT DEFAULT 0,
                is_premium BOOLEAN DEFAULT FALSE,
                season INT DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        # Farms table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS farms (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id BIGINT,
                level INT DEFAULT 1,
                production_rate INT DEFAULT 10,
                last_collection DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        # Items table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                description TEXT,
                type VARCHAR(50),
                rarity VARCHAR(50),
                price INT
            )
        """)

        self.connection.commit()

    def register_user(self, user_id, username):
        self.cursor.execute(
            "INSERT IGNORE INTO users (id, username) VALUES (%s, %s)",
            (user_id, username)
        )
        self.cursor.execute(
            "INSERT IGNORE INTO battle_pass (user_id) VALUES (%s)",
            (user_id,)
        )
        self.connection.commit()

    def get_user_data(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        return self.cursor.fetchone()

    def add_coins(self, user_id, amount):
        self.cursor.execute(
            "UPDATE users SET coins = coins + %s WHERE id = %s",
            (amount, user_id)
        )
        self.connection.commit()

    def spend_coins(self, user_id, amount):
        self.cursor.execute(
            "UPDATE users SET coins = coins - %s WHERE id = %s",
            (amount, user_id)
        )
        self.connection.commit()

    def add_experience(self, user_id, amount):
        self.cursor.execute(
            "UPDATE users SET experience = experience + %s WHERE id = %s",
            (amount, user_id)
        )
        self.check_level_up(user_id)
        self.connection.commit()

    def check_level_up(self, user_id):
        user = self.get_user_data(user_id)
        if user['experience'] >= 1000:
            new_level = user['level'] + 1
            remaining_exp = user['experience'] - 1000
            self.cursor.execute(
                "UPDATE users SET level = %s, experience = %s WHERE id = %s",
                (new_level, remaining_exp, user_id)
            )
            self.connection.commit()
            return True
        return False

    def add_energy(self, user_id, amount):
        self.cursor.execute("""
            UPDATE users 
            SET energy = LEAST(energy + %s, energy_max)
            WHERE id = %s
        """, (amount, user_id))
        self.connection.commit()

    def upgrade_mining(self, user_id):
        self.cursor.execute("""
            UPDATE users 
            SET mining_power = mining_power + 1
            WHERE id = %s
        """, (user_id,))
        self.connection.commit()

    def upgrade_energy_max(self, user_id):
        self.cursor.execute("""
            UPDATE users 
            SET energy_max = energy_max + 5,
                energy = energy + 5
            WHERE id = %s
        """, (user_id,))
        self.connection.commit()

    def update_after_training(self, user_id, coins, exp):
        self.cursor.execute("""
            UPDATE users 
            SET coins = coins + %s,
                experience = experience + %s,
                energy = energy - 1,
                total_trained = total_trained + 1
            WHERE id = %s
        """, (coins, exp, user_id))
        self.check_level_up(user_id)
        self.connection.commit()

    def add_mining_reward(self, user_id, coins):
        self.cursor.execute("""
            UPDATE users 
            SET coins = coins + %s,
                energy = energy - 1,
                total_mined = total_mined + %s
            WHERE id = %s
        """, (coins, coins, user_id))
        self.connection.commit()

    def get_user_inventory(self, user_id):
        self.cursor.execute("""
            SELECT i.*, it.name, it.description, it.type, it.rarity 
            FROM inventory i
            JOIN items it ON i.item_id = it.id
            WHERE i.user_id = %s
        """, (user_id,))
        return self.cursor.fetchall()

    def add_item_to_inventory(self, user_id, item_id):
        self.cursor.execute("""
            INSERT INTO inventory (user_id, item_id)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE quantity = quantity + 1
        """, (user_id, item_id))
        self.connection.commit()

    def get_farm_data(self, user_id):
        self.cursor.execute(
            "SELECT * FROM farms WHERE user_id = %s",
            (user_id,)
        )
        return self.cursor.fetchone()

    def create_farm(self, user_id):
        self.cursor.execute("""
            INSERT INTO farms (user_id, last_collection)
            VALUES (%s, CURRENT_TIMESTAMP)
        """, (user_id,))
        self.connection.commit()

    def upgrade_farm(self, user_id):
        self.cursor.execute("""
            UPDATE farms 
            SET level = level + 1,
                production_rate = production_rate * 1.5
            WHERE user_id = %s
        """, (user_id,))
        self.connection.commit()

    def collect_farm(self, user_id, coins):
        self.cursor.execute("""
            UPDATE farms 
            SET last_collection = CURRENT_TIMESTAMP
            WHERE user_id = %s
        """, (user_id,))
        self.add_coins(user_id, coins)
        self.connection.commit()

    def get_battle_pass_data(self, user_id):
        self.cursor.execute(
            "SELECT * FROM battle_pass WHERE user_id = %s",
            (user_id,)
        )
        return self.cursor.fetchone()

    def update_daily_reward(self, user_id, coins, energy):
        self.cursor.execute("""
            UPDATE users 
            SET coins = coins + %s,
                energy = LEAST(energy + %s, energy_max),
                last_daily = CURRENT_TIMESTAMP
            WHERE id = %s
        """, (coins, energy, user_id))
        self.connection.commit()

    def get_total_users(self):
        self.cursor.execute("SELECT COUNT(*) as count FROM users")
        return self.cursor.fetchone()['count']

    def get_total_coins(self):
        self.cursor.execute("SELECT SUM(coins) as total FROM users")
        return self.cursor.fetchone()['total']

    def get_premium_users_count(self):
        self.cursor.execute("SELECT COUNT(*) as count FROM battle_pass WHERE is_premium = TRUE")
        return self.cursor.fetchone()['count']

    def get_top_users(self, limit=10):
        self.cursor.execute("""
            SELECT id, username, coins, level, total_mined, total_trained 
            FROM users 
            ORDER BY coins DESC 
            LIMIT %s
        """, (limit,))
        return self.cursor.fetchall()

    def get_top_miners(self, limit=10):
        self.cursor.execute("""
            SELECT id, username, total_mined 
            FROM users 
            ORDER BY total_mined DESC 
            LIMIT %s
        """, (limit,))
        return self.cursor.fetchall()

    def get_top_trainers(self, limit=10):
        self.cursor.execute("""
            SELECT id, username, total_trained 
            FROM users 
            ORDER BY total_trained DESC 
            LIMIT %s
        """, (limit,))
        return self.cursor.fetchall()

    def get_top_battle_pass(self, limit=10):
        self.cursor.execute("""
            SELECT u.id, u.username, bp.level 
            FROM users u 
            JOIN battle_pass bp ON u.id = bp.user_id 
            ORDER BY bp.level DESC 
            LIMIT %s
        """, (limit,))
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.connection.close()
