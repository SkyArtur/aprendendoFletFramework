from ._singleton import *


class SQLiteConnector(Connector):
    """
    Concrete implementation of the Connector class for SQLite database connections.
    """

    def __init__(self, **kwargs):
        """
        Initializes the SQLiteConnector with connection parameters.
        """
        super().__init__(**kwargs)

    def connect(self) -> sqlite3.connect:
        """
        Establishes a connection to the SQLite database.

        Returns:
            sqlite3.connect: The SQLite connection object.
        """
        return sqlite3.connect(**self.params)


class MySQLConnector(Connector):
    """
    Concrete implementation of the Connector class for MySQL database connections.
    """

    def __init__(self, **kwargs):
        """
        Initializes the MySQLConnector with connection parameters.
        """
        super().__init__(**kwargs)

    def connect(self) -> mysql.connector.connect:
        """
        Establishes a connection to the MySQL database.

        Returns:
            mysql.connector.connect: The MySQL connection object.
        """
        return mysql.connector.connect(**self.params)


class PostgreSQLConnector(Connector):
    """
    Concrete implementation of the Connector class for PostgreSQL database connections.
    """

    def __init__(self, **kwargs):
        """
        Initializes the PostgreSQLConnector with connection parameters.
        """
        super().__init__(**kwargs)

    def connect(self) -> psycopg2.connect:
        """
        Establishes a connection to the PostgreSQL database.

        Returns:
            psycopg2.connect: The PostgreSQL connection object.
        """
        return psycopg2.connect(**self.params)