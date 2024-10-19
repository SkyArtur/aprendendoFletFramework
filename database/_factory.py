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
