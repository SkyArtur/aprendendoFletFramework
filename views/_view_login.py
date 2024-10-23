import flet as ft
from typing import Callable
from components import app_window, app_page, top_heading, text_field
from validators import validate_fields
from functions import make_login


def view_login(page: ft.Page, view_new_profile: Callable = None) -> None:
    def register_user(event):
        view_new_profile(page, view_login)

    def login(event):
        if not validate_fields(page, *_fields): return
        else:
            user = make_login(page, *_fields)
            print(user)


    page.controls.clear()
    app_window(page, 450, 550)
    app_page(page)
    top_heading(page, 'Login')
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    _fields = [
        text_field('Username', width=420),
        text_field('Password', width=420, password=True),
    ]
    page.add(
        ft.Container(
            ft.Row(controls=_fields, wrap=True),
            padding=ft.padding.only(top=25)
        ),
        ft.Container(
            ft.Column(
                controls=[
                    ft.ElevatedButton(
                        text='Login',
                        on_click=login,
                        width=250,
                        height=50,
                        bgcolor=ft.colors.INDIGO,
                        color=ft.colors.WHITE
                    ),
                    ft.TextButton(
                        text='New User',
                        on_click=register_user,
                        width=200,
                        height=40,
                        style=ft.ButtonStyle(color=ft.colors.BLACK)
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15
            ),
            padding=ft.padding.only(top=25),
        )
    )
    page.update()