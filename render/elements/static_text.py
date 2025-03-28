from rich import box
from rich.panel import Panel
from render.window import Window


class StaticText(Window):

    def __init__(self, text, style=""):
        super().__init__()
        self.text = text
        self.style = style

    def render(self):
        return Panel(self.text, style=self.style, box=box.SIMPLE_HEAD)
