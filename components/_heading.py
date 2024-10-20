from components import *


def top_heading(page: Page, text: str):
    foreground = Paint(color=colors.INDIGO, stroke_width=6, stroke_join=StrokeJoin.ROUND,style=PaintingStyle.STROKE)
    stack_1 = Text(spans=[TextSpan(text, TextStyle(size=32,weight=FontWeight.BOLD,foreground=foreground))])
    stack_2 = Text(spans=[TextSpan(text, TextStyle(size=32, weight=FontWeight.BOLD, color=colors.WHITE))])
    page.add(Column(controls=[Stack([stack_1, stack_2]), Divider()], horizontal_alignment=CrossAxisAlignment.CENTER))
