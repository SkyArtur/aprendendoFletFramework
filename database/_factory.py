from typing import Literal
from ._objects import SQLiteConnector, MySQLConnector, PostgreSQLConnector


class Database:
    """
    Provides a Singleton interface for selecting and using different database connectors.

    Attributes:
        __instance (Connector): The single instance of the chosen database connector.
    """
    __instance = None

    def __new__(cls, __driver: Literal['sqlite', 'mysql','postgres'], *args, **kwargs):
        """
        Selects the appropriate database connector based on the provided driver.

        Args:
            __driver (Literal['sqlite', 'mysql', 'postgres']): The database driver type.
            *args: Positional arguments for the database connector.
            **kwargs: Keyword arguments for the database connector.

        Returns:
            Connector: The selected database connector instance.

        Raises:
            ValueError: If an unsupported database driver is provided.
        """
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
