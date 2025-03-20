from rich import box
from rich.table import Table
from render.raw_window import RawWindow


class List(RawWindow):

    def __init__(self, title):
        super().__init__()
        self.title = title
        self.elements = []

    def add(self, element):
        self.elements.append(element)

    def __rich_console__(self, console, options):
        table = Table(expand=True,
                      box=box.ROUNDED,
                      pad_edge=True,
                      show_edge=True,
                      show_header=True)

        table.add_column("Rewrite rules")
        for element in self.elements:
            table.add_row(element)

        max_height = (console.height - 7) - len(self.elements)

        for i in range(max_height):
            table.add_row("")
        yield table
