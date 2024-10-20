from typing import Callable
from components import snack_bar, Page


def decorator_validators(function: Callable) -> Callable:
    """
    A decorator that wraps a function to catch and handle exceptions during input validation.

    Args:
        function (Callable): The function to be decorated.

    Returns:
        Callable: A wrapped version of the input function that handles exceptions using a snack bar.
    """
    def _wrapper(page: Page, *args, **kwargs):
        try:
            _input = function(page, *args, **kwargs)
        except Exception as e:
            snack_bar(page, f'{e}', function)
        else:
            return _input
    return _wrapper