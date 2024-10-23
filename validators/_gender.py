from ._decorator import decorator_validators
from components import Page, Dropdown


@decorator_validators
def validate_gender(page: Page, gender: Dropdown) -> None:
    if not gender.value in 'FM':
        raise ValueError(f'Invalid gender: {gender.value}')
    return gender.value
