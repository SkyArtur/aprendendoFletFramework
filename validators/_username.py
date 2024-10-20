from database import dbDev
from components import  Page, TextField
from ._decorator import decorator_validators


@decorator_validators
def validate_username(page: Page, _username: TextField) -> str | None:
    """
    Validates the uniqueness of the username in the database.

    Args:
        page (Page): The page on which the validation occurs.
        _username (TextField): The TextField containing the username to be validated.

    Returns:
        str | None: Returns the username if valid, raises a ValueError if it already exists.

    Raises:
        ValueError: If the username already exists in the database.
    """
    if dbDev.fetch('SELECT id FROM users WHERE username = %s;', (_username.value,)):
        raise ValueError('Username already exists')
    return _username.value
