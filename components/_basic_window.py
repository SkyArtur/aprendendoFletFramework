from flet_core import Page, alignment


def basic_window(page: Page, height: int, width: int) -> None:
    page.window.height = height
    page.window.width = width
    page.window.resizable = False
    page.window.maximizable = False
    page.window.alignment = alignment.top_right
    page.update()