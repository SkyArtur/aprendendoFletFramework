from typing import Callable
from components import snack_bar, Page


def decorator_validators(function: Callable) -> Callable:
    def _wrapper(page: Page, *args, **kwargs):
        try:
            _input = function(page, *args, **kwargs)
        except Exception as e:
            snack_bar(page, f'{e}', function)
        else:
            return _input
    return _wrapper