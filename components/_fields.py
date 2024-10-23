from components import Page, TextField, InputBorder, TextStyle, colors


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