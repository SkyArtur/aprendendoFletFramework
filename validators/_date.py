import re
import datetime
from typing import Literal
from components import  Page, TextField
from ._decorator import decorator_validators


@decorator_validators
def validate_date(page: Page, _date: TextField, _format: Literal['UK', 'US', 'ISO'] = 'UK') -> datetime.date:
    """
    Validates the date format and converts the input string into a datetime.date object.

    Args:
        page (Page): The page on which the validation occurs.
        _date (TextField): The TextField containing the date string to be validated.
        _format (Literal['UK', 'US', 'ISO'], optional): The date format to use for parsing. Defaults to 'UK'.

    Returns:
        datetime.date: Returns a date object if the input is valid, raises a ValueError if invalid.

    Raises:
        ValueError: If the input string does not match the expected date format.
        Exception: If the input date string is not valid.
    """
    try:
        date = [int(i) for i in re.search(r'^([0-9]{2,4})[/-]?([0-9]{2})[/-]?([0-9]{2,4})$', _date.value).groups()]
        match _format:
            case 'UK':
                return datetime.date(day=date[0], month=date[1], year=date[2])
            case 'US':
                return datetime.date(day=date[1], month=date[0], year=date[2])
            case 'ISO':
                return datetime.date(day=date[2], month=date[1], year=date[0])
            case _:
                raise ValueError('Invalid date format')
    except (ValueError, AttributeError) as error:
        if isinstance(error, AttributeError):
            raise Exception(f'Invalid date string')
        else:
            raise error
