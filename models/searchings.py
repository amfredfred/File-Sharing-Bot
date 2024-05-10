from database.connection import DBConnection
from helper_func import most_common_word

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
                searched_for TEXT,
                downloads INTEGER DEFAULT 0
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

    def increment_downloads(self, searched_for):
        query = "UPDATE searchings SET downloads = downloads + 1 WHERE searched_for = %s"
        with self.conn.cursor() as cursor:
            cursor.execute(query, (searched_for,))
            self.conn.commit()
            return cursor.rowcount

    def most_common_searched_word(self):
        searched_for_texts = [row[2] for row in self.get_all_searchings()]
        combined_text = ' '.join(searched_for_texts)
        return most_common_word(combined_text)
