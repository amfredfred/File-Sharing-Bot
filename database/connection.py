from config import POSTGRESQL_CONNECTION_STRING
import psycopg2


class DBConnection:

    def __init__(self, connection_string: str = POSTGRESQL_CONNECTION_STRING) -> None:
        self.instance = psycopg2.connect(connection_string)

    def conneciton(self):
        return self.instance
