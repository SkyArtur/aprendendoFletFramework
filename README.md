# Aprendendo Flet - Python

Conhecendo o framework [Flet](https://flet.dev/) para criação de aplicações multi plataformas.

## Conexão com o banco de dados

### Classe Connector:
É a classe base abstrata que define a interface para conectar e executar operações nos diferentes bancos de dados 
(SQLite, MySQL, PostgreSQL). Usa o padrão Singleton para garantir que apenas uma instância da conexão seja criada.

- **Método __execute**: É responsável por executar consultas no banco de dados, podendo realizar operações de fetch (busca) 
ou commit (salvamento). Ele gerencia exceções específicas de diferentes tipos de banco de dados e garante que os 
cursores e conexões sejam fechados corretamente no final.

```python
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
```

### Subclasses SQLiteConnector, MySQLConnector, PostgreSQLConnector: 
São subclasses da classe Connector que implementam o método abstrato connect para fornecer conexões específicas aos 
bancos de dados correspondentes.
```python
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
```
### Classe Database: 
Também segue o padrão Singleton e seleciona o conector adequado com base no driver fornecido (sqlite, mysql ou postgres).

```python
from typing import Literal
from ._objects import SQLiteConnector, MySQLConnector, PostgreSQLConnector


class Database:
    __instance = None

    def __new__(cls, __driver: Literal['sqlite', 'mysql','postgres'], *args, **kwargs):
        if cls.__instance is None:
            match __driver:
                case 'sqlite':
                    cls.__instance = SQLiteConnector(**kwargs)
                case 'mysql':
                    cls.__instance = MySQLConnector(**kwargs)
                case 'postgres':
                    cls.__instance = PostgreSQLConnector(**kwargs)
                case _:
                    raise ValueError(f'Unsupported database driver: {__driver}')
        return cls.__instance
```



