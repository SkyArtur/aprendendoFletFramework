from typing import Callable
from components import *


def snack_bar(page: Page, message: str, function: Callable) -> None:
    origin = TextSpan(text=f'Error <{function.__name__}>: ', style=TextStyle(color=colors.RED_300))
    message = TextSpan(text=message.upper(), style=TextStyle(color=colors.WHITE))
    snack_tex = Text(spans=[origin, message], weight=FontWeight.BOLD)
    snack = SnackBar(snack_tex, bgcolor=colors.INDIGO, show_close_icon=True, close_icon_color=colors.WHITE, open=True)
    page.overlay.clear()
    page.overlay.append(snack)
    page.update()
