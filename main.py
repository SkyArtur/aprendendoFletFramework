import flet as ft
from views import view_new_profile


def main(page: ft.Page):
    view_new_profile(page)


if __name__ == '__main__':
    ft.app(target=main)