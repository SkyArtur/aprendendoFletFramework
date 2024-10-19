from ._singleton import *


class SQLiteConnector(Connector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def connect(self) -> sqlite3.connect:
        return sqlite3.connect(**self.params)


class MySQLConnector(Connector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def connect(self) -> mysql.connector.connect:
        return mysql.connector.connect(**self.params)


class PostgreSQLConnector(Connector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def connect(self) -> psycopg2.connect:
        return psycopg2.connect(**self.params)