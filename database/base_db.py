import mysql.connector
from config.config import DB_CONFIG

class BaseDatabase:
    def __init__(self):
        self.connection = mysql.connector.connect(**DB_CONFIG)
        self.cursor = self.connection.cursor(dictionary=True)
        self.connection.autocommit = True
        
    def execute_query(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor
        
    def fetch_one(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor.fetchone()
        
    def fetch_all(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor.fetchall()
        
    def __del__(self):
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
