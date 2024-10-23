from passlib.hash import pbkdf2_sha256 as pbkdf2
from database import dbDev
from components import snack_bar, TextField, Page



def make_login(page: Page, _username: TextField, _password: TextField):

    try:
        query = """
        SELECT u.id, p.name, p.birth, u.username, u.email, u.password 
        FROM users u JOIN profiles p ON u.id = p.id_user
        WHERE username = %s or email = %s
        """
        user = dbDev.fetch(query, (_username.value, _username.value))[0]
        if not user:
            raise ValueError("User does not exist!")
        if not pbkdf2.verify(_password.value, user[5]):
            raise ValueError("Invalid password!")
    except ValueError as error:
        snack_bar(page, f'{error}.', make_login)
    else:
        return user[:5]