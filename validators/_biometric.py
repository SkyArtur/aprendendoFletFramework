from typing import Literal
from components import Page, TextField
from ._decorator import decorator_validators


@decorator_validators
def validate_biometric(page: Page, _field: TextField, _biometric: Literal['weight', 'height']) -> float:
    """
    Validate biometric data, either weight or height, ensuring the value is within a specific range.

    Args:
        page (Page): The current page or UI context in which the validation is being performed.
        _field (TextField): The input field containing the value to be validated, either representing weight or height.
        _biometric (Literal['weight', 'height']): A string literal indicating whether the field corresponds to
            'weight' (in kilograms) or 'height' (in meters).

    Returns:
        float: The validated value of the biometric data (weight or height) if it is within the valid range.

    Raises:
        ValueError: If the provided value for weight is not between 0 and 300 kg, or for height if not between 0 and 3 meters.
                   Also raised if the biometric type is invalid or unsupported.

    Examples:
        >> validate_biometric(page, weight_field, 'weight')
        75.0

        >> validate_biometric(page, height_field, 'height')
        1.75

    Notes:
        - The function expects the input value to be in string format and converts it to a float, replacing commas
          with dots to handle decimal numbers.
        - The `@decorator_validators` handles error reporting through a notification system in the UI (e.g., using
          a snack bar).
    """
    value = float(_field.value.replace(',', '.'))
    match _biometric:
        case 'weight':
            if value < 0 or value > 300:
                raise ValueError(f'Value {value} must be between 0 and 300')
        case 'height':
            if value < 0 or value > 3:
                raise ValueError(f'Value {value} must be between 0 and 3')
        case _:
            raise ValueError(f'Invalid value for {_field}')
    return value
