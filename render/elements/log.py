from rich import box
from rich.table import Table
from rich.panel import Panel
from render.raw_window import RawWindow


class Log(RawWindow):

    def __init__(self):
        super().__init__()
        self.entries = []

    def log(self, element, operation=None):
        self.entries.append((element, operation))

    def __rich_console__(self, console, options):
        table = Table.grid(expand=True)

        table.add_column("entry", justify="left", ratio=1)
        table.add_column("operation", justify="center")
        for entry, operation in self.entries:
            if operation is None:
                operation = ""
            else:
                operation = "∵ " + operation
            table.add_row(entry, operation)

        max_height = (console.height - 11) - len(self.entries)

        for i in range(max_height):
            table.add_row("", "")

        yield Panel(table, box=box.ROUNDED)
