from datetime import datetime, timedelta
from database.connection import DBConnection

class Profile:

    def __init__(self):
        db_connect = DBConnection()
        self.conn = db_connect.conneciton()
        self._create_table()

    def _create_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS profiles (
                id SERIAL PRIMARY KEY,
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
                deleted_at TIMESTAMPTZ,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
            )
        """
        with self.conn.cursor() as cursor:
            cursor.execute(query)
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
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
            with self.conn.cursor() as cursor:
                cursor.execute(query, values)
                self.conn.commit()
                return True
        except Exception as e:
            self.conn.rollback()
            return False

    def get_profile_by_telegram_id(self, telegram_id):
        query = (
            f"SELECT * FROM profiles WHERE telegram_id = CAST({telegram_id} AS TEXT)"
        )
        with self.conn.cursor() as cursor:
            cursor.execute(query, (telegram_id,))
            return cursor.fetchone()

    def get_all_users(self):
        query = "SELECT * FROM profiles"
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def delete_profile(self, telegram_id):
        query = f"DELETE FROM profiles WHERE telegram_id = CAST({telegram_id} AS TEXT)"
        with self.conn.cursor() as cursor:
            cursor.execute(query, (telegram_id,))
            self.conn.commit()
            return cursor.rowcount
        
    def get_active_users_last_24_hours(self): 
        twenty_four_hours_ago = datetime.now() - timedelta(hours=24) 
        query = "SELECT * FROM profiles WHERE updated_at >= %s"
        
        with self.conn.cursor() as cursor:
            cursor.execute(query, (twenty_four_hours_ago,))
            return cursor.fetchall()
