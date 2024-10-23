import sqlite3
import psycopg2
import mysql.connector
from abc import abstractmethod


class Connector:
    """
    Abstract base class that provides a Singleton pattern for database connections.
    Defines basic operations for interacting with databases.

    Attributes:
        params (dict): Connection parameters passed during initialization.
        __cursor (Cursor): The database cursor for executing queries.
        __connection (Connection): The active database connection.
        __response (list): The response from fetch operations.
    """
    __instance = None

    def __new__(cls, *args, **kwargs):
        """
        Ensures only one instance of the Connector class is created (Singleton pattern).
        """
        if cls.__instance is None:
            cls.__instance = super(Connector, cls).__new__(cls)
        return cls.__instance


    def __init__(self, **kwargs):
        """
        Initializes the connector with the given connection parameters.

        Args:
            kwargs: Keyword arguments representing database connection parameters.
        """
        self.params = kwargs
        self.__cursor = None
        self.__connection = None
        self.__response = None

    @abstractmethod
    def connect(self):
        """
        Abstract method that must be implemented by subclasses to establish a database connection.
        """
        ...

    def __execute(self, query: str, data: tuple = None, fetch: bool = False, commit: bool = False) -> list[tuple] | None:
        """
        Executes a SQL query on the database and handles fetch or commit operations.

        Args:
            query (str): The SQL query to be executed.
            data (tuple, optional): Data to be passed into the query, if any.
            fetch (bool, optional): Whether to fetch the result of the query. Defaults to False.
            commit (bool, optional): Whether to commit the transaction. Defaults to False.

        Returns:
            list[tuple] | None: The fetched result, if applicable, or None.

        Raises:
            Exception: If any database error occurs.
        """
        try:
            self.__connection = self.connect()
            self.__cursor = self.__connection.cursor()
            self.__cursor.execute(query, data) if data else self.__cursor.execute(query)
        except (psycopg2.Error, mysql.connector.Error, sqlite3.Error, Exception) as error:
            raise Exception(error)
        else:
            if fetch:
                self.__response = self.__cursor.fetchall()
            if commit:
                self.__connection.commit()
            return self.__response
        finally:
            try:
                self.__cursor.close()
                self.__connection.close()
            except (psycopg2.Error, mysql.connector.Error, sqlite3.Error, Exception) as error:
                raise Exception(error)

    def create(self, query: str):
        """
        Creates a new table or executes a similar schema-altering query.

        Args:
            query (str): The SQL query to create a table or perform schema operations.
        """
        self.__execute(query, commit=True)

    def save(self, query: str, data: tuple):
        """
        Inserts or updates data in the database.

        Args:
            query (str): The SQL query for inserting or updating.
            data (tuple): The data to be inserted or updated.

        Returns:
            list[tuple] | None: The result of the query execution.
        """
        return self.__execute(query, data, commit=True, fetch=True)

    def fetch(self, query: str, data: tuple = None):
        """
        Fetches data from the database.

        Args:
            query (str): The SQL query for fetching data.
            data (tuple, optional): Parameters for the query, if needed.

        Returns:
            list[tuple] | None: The fetched result, or None if no result was found.
        """
        return self.__execute(query, data, fetch=True)