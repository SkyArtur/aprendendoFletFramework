from components import Page, TextField


def clear_fields(page: Page, *args: TextField) -> None:
    for field in args:
        field.value = None
    page.update()
