import re
from database import dbDev
from components import  Page, TextField
from ._decorator import decorator_validators


@decorator_validators
def validate_email(page: Page, _email: TextField) -> str | None:
    """
    Validates the email format and checks for uniqueness in the database.

    Args:
        page (Page): The page on which the validation occurs.
        _email (TextField): The TextField containing the email to be validated.

    Returns:
        str | None: Returns the email if valid, raises a ValueError if invalid or already registered.

    Raises:
        ValueError: If the email is already registered.
        Exception: If the email format is invalid.
    """
    try:
        email = re.search(r'^[a-z0-9_.+-]+@([a-z0-9-]+\.)+[a-z]{2,}$', _email.value).string
        if dbDev.fetch('SELECT id FROM users WHERE email = %s;', (email,)):
            raise ValueError('Email already registered!')
    except (TypeError, ValueError, AttributeError) as error:
        if isinstance(error, AttributeError):
            error = Exception('Value is not valid for a email')
        raise error
    else:
        return email
