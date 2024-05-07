import psycopg2
from database.connection import DBConnection

class Searching:
    def __init__(self):
        db_connect = DBConnection()
        self.conn = db_connect.conneciton()
        self._create_table()

    def _create_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS searchings (
                id SERIAL PRIMARY KEY,
                chat_id INTEGER,
                searched_for TEXT
            )
        """
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            self.conn.commit()

    def insert_searching(self, chat_id, searched_for):
        try:
            query = """
            INSERT INTO searchings
                (chat_id, searched_for)
            VALUES
                (%s, %s)
            """
            values = (chat_id, searched_for)
            with self.conn.cursor() as cursor:
                cursor.execute(query, values)
                self.conn.commit()
                print("Saved")
                return True
        except Exception as e:
            print(f"Exception: {e}")
            self.conn.rollback()
            return False

    def get_searching_by_searched_for(self, searched_for):
        query = "SELECT * FROM searchings WHERE searched_for = %s"
        with self.conn.cursor() as cursor:
            cursor.execute(query, (searched_for,))
            return cursor.fetchone()

    def get_all_searchings(self):
        query = "SELECT * FROM searchings"
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def delete_searching(self, searched_for):
        query = "DELETE FROM searchings WHERE searched_for = %s"
        with self.conn.cursor() as cursor:
            cursor.execute(query, (searched_for,))
            self.conn.commit()
            return cursor.rowcount
