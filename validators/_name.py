from components import  Page, TextField
from ._decorator import decorator_validators


@decorator_validators
def validate_name(page: Page, _name: TextField) -> str | None:
    """
    Validates that the name is a non-empty alphanumeric string.

    Args:
        page (Page): The page on which the validation occurs.
        _name (TextField): The TextField containing the name to be validated.

    Returns:
        str | None: Returns the name if valid, raises a ValueError if invalid.

    Raises:
        ValueError: If the name contains non-alphanumeric characters or is not a string.
    """
    if not isinstance(_name.value, str) or not _name.value.replace(' ', '').isalnum():
        raise ValueError(f'Value entered in the {_name.label} field is not valid')
    return _name.value
