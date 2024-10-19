import sqlite3
import psycopg2
import mysql.connector
from abc import abstractmethod


class Connector:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Connector, cls).__new__(cls)
        return cls.__instance


    def __init__(self, **kwargs):
        self.params = kwargs
        self.__cursor = None
        self.__connection = None
        self.__response = None

    @abstractmethod
    def connect(self):
        ...

    def __execute(self, query: str, data: tuple = None, fetch: bool = False, commit: bool = False) -> list[tuple] | None:
        try:
            self.__connection = self.connect()
            self.__cursor = self.__connection.cursor()
            self.__cursor.execute(query, data) if data else self.__cursor.execute(query)
        except (psycopg2.Error, mysql.connector.Error, sqlite3.Error, Exception) as error:
            return error
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
                return error

    def create(self, query: str):
        self.__execute(query, commit=True)

    def save(self, query: str, data: tuple):
        return self.__execute(query, data, commit=True, fetch=True)

    def fetch(self, query: str, data: tuple = None):
        return self.__execute(query, data, fetch=True)