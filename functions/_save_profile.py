from database import dbDev
from components import snack_bar, Page


def save_profile(page: Page, name, birth, username, email, password, weight, height, /) -> None:
    try:
        query = 'CALL create_profile(%s, %s, %s, %s, %s, %s, %s);'
        dbDev.save(query, (name, birth, username, email, password, weight, height))
    except Exception as error:
        snack_bar(page, f'{error}.', save_profile)
