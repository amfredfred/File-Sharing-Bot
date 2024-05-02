import sqlite3
from config import SQLITE_DB_FILE

class profile:

    def __init__(self, db_file=SQLITE_DB_FILE):
        self.conn = sqlite3.connect(db_file)
        self.create_table()

    def create_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS profiles (
                id INTEGER PRIMARY KEY,
                chat_id INTEGER,
                telegram_id TEXT UNIQUE,
                username TEXT UNIQUE,
                first_name TEXT,
                last_name TEXT,
                level INTEGER,
                bio TEXT,
                location TEXT,
                avatar TEXT,
                website TEXT,
                deleted_at TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        """
        self.conn.execute(query)
        self.conn.commit()

    def insert_profile(
        self,
        chat_id,
        telegram_id,
        username=None,
        first_name=None,
        last_name=None,
        level=None,
        bio=None,
        location=None,
        avatar=None,
        website=None,
    ):
        try:
            query = """
            INSERT INTO profiles
                (chat_id, telegram_id, username, first_name, last_name, level, bio, location, avatar, website)
            VALUES
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            values = (
                chat_id,
                telegram_id,
                username,
                first_name,
                last_name,
                level,
                bio,
                location,
                avatar,
                website,
            )
            self.conn.execute(query, values)
            account = self.conn.commit()
            return account
        except Exception as e:
            self.conn.rollback()
            return False

    def get_profile_by_telegram_id(self, telegram_id):
        query = "SELECT * FROM profiles WHERE telegram_id = ?"
        cursor = self.conn.execute(query, (telegram_id,))
        return cursor.fetchone()

    def get_all_users(self):
        query = "SELECT * FROM profiles"
        cursor = self.conn.execute(query)
        return cursor.fetchall()

    def delete_profile(self, telegram_id):
        query = "DELETE FROM profiles WHERE telegram_id = ?"
        self.conn.execute(query, (telegram_id,))
        self.conn.commit()
        return self.cursor.rowcount
