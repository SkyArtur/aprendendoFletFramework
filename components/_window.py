from components import *


def app_window(page: Page, width: int, height: int) -> None:
    page.window.height = height
    page.window.width = width
    page.window.resizable = False
    page.window.maximizable = False
    page.window.alignment = alignment.top_right
    page.update()
