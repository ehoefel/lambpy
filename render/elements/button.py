from rich.panel import Panel
from render.window import Window


class Button(Window):

    def __init__(self, text, style, disabled_style=""):
        super().__init__()
        self.text = text
        self.style = style
        self.disabled_style = disabled_style

    def render(self):

        style = self.style + " bold"
        if not self.is_active():
            style += " dim"
        if not self.is_enabled():
            style = self.disabled_style

        return Panel(self.text, style=style, border_style=style)
