from components import Text, Dropdown, TextField, InputBorder, TextStyle, colors, dropdown


def text_field(label: str, width: int = 100, password: bool = False, *args, **kwargs) -> TextField:
    return TextField(
        label=label,
        label_style=TextStyle(color=colors.INDIGO),
        width=width,
        color=colors.BLACK,
        border=InputBorder.UNDERLINE,
        password=password,
        can_reveal_password=password,
        *args,
        **kwargs
    )

def dropdown_field(label: str,options: list[str], width: int = 100, *args, **kwargs) -> Dropdown:
    return Dropdown(
        label=label,
        label_style=TextStyle(color=colors.INDIGO),
        icon_enabled_color=colors.INDIGO,
        options=[dropdown.Option(o) for o in options],
        width=width,
        color=colors.BLACK,
        bgcolor=colors.BLUE_GREY_50,
        border=InputBorder.UNDERLINE,
        *args,
        **kwargs
    )