import psycopg2
from config import POSTGRESQL_CONNECTION_STRING

class Profile:

    def __init__(self, connection_string=POSTGRESQL_CONNECTION_STRING):
        self.conn = psycopg2.connect(connection_string)
        self.create_table()

    def create_table(self):
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
        query = "SELECT * FROM profiles WHERE telegram_id = %s"
        with self.conn.cursor() as cursor:
            cursor.execute(query, (telegram_id,))
            return cursor.fetchone()

    def get_all_users(self):
        query = "SELECT * FROM profiles"
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def delete_profile(self, telegram_id):
        query = "DELETE FROM profiles WHERE telegram_id = %s"
        with self.conn.cursor() as cursor:
            cursor.execute(query, (telegram_id,))
            self.conn.commit()
            return cursor.rowcount
