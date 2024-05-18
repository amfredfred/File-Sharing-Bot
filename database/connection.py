from config import (
    POSTGRESQL_CONNECTION_STRING,
    POSTGRESQL_USERNAME,
    POSTGRESQL_PASSWORD,
    POSTGRESQL_HOST,
    POSTGRESQL_DB,
)
import psycopg2

from sqlalchemy import create_engine

class DBConnection:
    def __init__(self) -> None:
        self.engine = self.create_postgres_engine(
            POSTGRESQL_USERNAME, POSTGRESQL_PASSWORD, POSTGRESQL_HOST, POSTGRESQL_DB
        )

    def connection(self):
        return psycopg2.connect(POSTGRESQL_CONNECTION_STRING)

    @staticmethod
    def create_postgres_engine(username, password, host, database_name):
        connection_string = f"postgresql://{username}:{password}@{host}/{database_name}"
        return create_engine(connection_string)


engine = DBConnection().engine