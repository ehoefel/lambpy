from rich.panel import Panel
from render.window import Window


class Button(Window):

    def __init__(self, text, style):
        super().__init__()
        self.text = text
        self.style = style

    def render(self, focused):

        style = self.style + " bold"
        if not focused:
            style += " dim"

        return Panel(self.text, style=style, border_style=style)
