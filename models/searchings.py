import sqlite3

from dotenv import load_dotenv

load_dotenv()
import os

SQLITE_DB_FILE = os.getenv("SQLITE_DB_FILE")


class searching:
    def __init__(self, db_file=SQLITE_DB_FILE):
        self.conn = sqlite3.connect(db_file)
        self.create_table()

    def create_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS searchings (
                id INTEGER PRIMARY KEY,
                chat_id INTEGER,
                searched_for TEXT
            )
        """
        self.conn.execute(query)
        self.conn.commit()

    def insert_searching(self, chat_id,searched_for):
        try:
            query = """
            INSERT INTO searchings
                (chat_id, searched_for)
            VALUES
                (?, ?)
            """
            values = (
                chat_id,
                searched_for
            )
            self.conn.execute(query, values)
            searched = self.conn.commit()
            print('saved')
            return searched
        except Exception as e:
            print(f"Exception: {e}")
            self.conn.rollback()
            return False

    def get_searching_by_searched_for(self, searched_for):
        query = "SELECT * FROM searchings WHERE searched_for = ?"
        cursor = self.conn.execute(query, (searched_for,))
        return cursor.fetchone()

    def get_all_seachings(self):
        query = "SELECT * FROM searchings"
        cursor = self.conn.execute(query)
        return cursor.fetchall()

    def delete_searching(self, searched_for):
        query = "DELETE FROM searchings WHERE searched_for = ?"
        self.conn.execute(query, (searched_for,))
        self.conn.commit()
        return self.cursor.rowcount
