import flet as ft
from typing import Callable
from components import app_window, app_page, top_heading, text_field
from validators import *
from functions import clear_fields, save_profile


def view_new_profile(page: ft.Page, view_login: Callable) -> None:

    def save(event):
        if not validator_fields(page, *_fields): return
        elif not (_name := validate_name(page, _fields[0])): return
        elif not (_birth := validate_date(page, _fields[1])): return
        elif not (_username := validate_username(page, _fields[2])): return
        elif not (_email := validate_email(page, _fields[3])): return
        elif not (_password := validate_password(page, _fields[4], _fields[5])): return
        elif not (_weight := validate_biometric(page, _fields[6], 'weight')): return
        elif not (_height := validate_biometric(page, _fields[7], 'height')): return
        else:
            save_profile(page, _name, _birth, _username, _email, _password, _weight, _height)
        clear_fields(page, *_fields)

    app_window(page, 700, 490)
    app_page(page)
    top_heading(page, 'Register a new user')
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    _fields = [
        text_field('Name', width=440, tooltip='Alphabetic characters only.'),
        text_field('Birth Date', width=200, hint_text='DD/MM/YYYY'),
        text_field('Username', width=200),
        text_field('Email', width=440, hint_text='example@email.com'),
        text_field('Password', width=318, password=True, tooltip='Minimum of 6 characters.'),
        text_field('Confirm Password', width=318, password=True),
        text_field('Weight', width=160, suffix_text='kilograms', tooltip='Use a comma (,) to separate decimal places.'),
        text_field('Height', width=160, suffix_text='meters', tooltip='Use a comma (,) to separate decimal places.'),
    ]
    btn = ft.ElevatedButton('click', on_click=save, width=200, height=40, bgcolor=ft.colors.INDIGO, color=ft.colors.WHITE)
    page.add(
        ft.Row(controls=_fields[:2], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row(controls=_fields[2:4], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row(controls=_fields[4:6], alignment=ft.MainAxisAlignment.CENTER),
        ft.Container(ft.Row(controls=_fields[6:]), padding=ft.padding.only(left=10, bottom=25)),
        ft.Row(controls=[btn], alignment=ft.MainAxisAlignment.CENTER)
    )
    page.update()

