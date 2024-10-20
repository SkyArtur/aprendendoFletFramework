from typing import Callable
from components import *


def snack_bar(page: Page, message: str, function: Callable) -> None:
    origin = TextSpan(text=f'ERROR :: {function.__name__} :: \t', style=TextStyle(color=colors.RED_200, size=10))
    message = TextSpan(text=message.capitalize(), style=TextStyle(color=colors.WHITE, size=18))
    snack_tex = Text(spans=[origin, message], weight=FontWeight.BOLD)
    snack = SnackBar(snack_tex, bgcolor=colors.INDIGO, show_close_icon=True, close_icon_color=colors.WHITE, open=True)
    page.overlay.clear()
    page.overlay.append(snack)
    page.update()
