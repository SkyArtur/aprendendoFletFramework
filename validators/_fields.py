from components import  Page, TextField
from ._decorator import decorator_validators


@decorator_validators
def validate_fields(page: Page, *args: TextField) -> bool | None:
    """
    Validates that each TextField is not empty or null.

    Args:
        page (Page): The page on which the validation occurs.
        *args (TextField): Variable number of TextField inputs to validate.

    Returns:
        bool | None: Returns True if all fields are valid, raises a ValueError if any field is empty.

    Raises:
        ValueError: If any field is null or empty.
    """
    for text_field in args:
        if text_field.value is None or text_field.value == '':
            raise ValueError(f'Field "{text_field.label}" cannot be null')
    return True
