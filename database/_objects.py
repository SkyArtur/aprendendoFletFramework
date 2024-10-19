import os
from dotenv import load_dotenv
from pathlib import Path
from ._singleton import *


load_dotenv(dotenv_path=Path(__file__).parent.parent / '.env')


class SQLiteConnector(Connector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not kwargs:
            self.params = {'database': f'{os.getenv("DATABASE")}.sqlite3'}

    def connect(self) -> sqlite3.connect:
        return sqlite3.connect(**self.params)


class MySQLConnector(Connector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not kwargs:
            self.params = {
                'database': os.getenv('DATABASE'),
                'user': os.getenv('USER'),
                'password': os.getenv('PASSWORD'),
            }

    def connect(self) -> mysql.connector.connect:
        return mysql.connector.connect(**self.params)


class PostgreSQLConnector(Connector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not kwargs:
            self.params = {
                'database': os.getenv('DATABASE'),
                'user': os.getenv('USER'),
                'password': os.getenv('PASSWORD'),
            }

    def connect(self) -> psycopg2.connect:
        return psycopg2.connect(**self.params)