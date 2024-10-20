from passlib.hash import pbkdf2_sha256 as pbk
from components import  Page, TextField
from ._decorator import decorator_validators



@decorator_validators
def validate_password(page: Page, _password: TextField, _confirm: TextField) -> str | None:
    """
    Validates the password and its confirmation, ensuring they match and meet length requirements.

    Args:
        page (Page): The page on which the validation occurs.
        _password (TextField): The TextField containing the password.
        _confirm (TextField): The TextField containing the password confirmation.

    Returns:
        str | None: Returns the hashed password if valid, raises a ValueError if invalid.

    Raises:
        ValueError: If the password is less than 6 characters or does not match the confirmation.
    """
    if len(_password.value) < 6:
        raise ValueError('Password must be at least 6 characters')
    elif _password.value != _confirm.value:
        raise ValueError('Confirm password must equal password')
    else:
        return pbk.hash(_password.value)
