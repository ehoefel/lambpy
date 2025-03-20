from rich.layout import Layout
from rich.live import Live

# frame = 0
fps = 10


def make_layout() -> Layout:
    layout = Layout(name="root")

    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body", ratio=1)
    )

    layout['header'].split_row(
        Layout(name="logo", size=5),
        Layout(name="title", ratio=1),
        Layout(name="buttons", size=21)
    )
    layout["buttons"].split_row(Layout(name="help"), Layout(name="info"))

    layout['body'].split_row(
        Layout(name="main", ratio=1),
        Layout(name="rewrites", size=30)
    )

    layout["main"].split_column(
        Layout(name="input_area", size=3),
        Layout(name="output", ratio=1),
        Layout(name="footer", size=3),
    )

    layout["input_area"].split_row(
        Layout(name="input", ratio=1),
        Layout(name="start", size=9)
    )

    layout["footer"].split_row(
        Layout(name="next", size=13),
        Layout(name="footer_middle", ratio=1),
        Layout(name="save", size=8)
    )

    return layout


class Renderer:

    def __init__(self):
        self.update = None
        self.layout = make_layout()
        pass

    def layout_update(self, fn):
        fn(self.layout)

    def set_shared_variables(self, ref):
        global shared_variables
        shared_variables = ref

    def on_update(self, fn):
        self.update = fn

    def __call__(self):
        import time
        with Live(self.layout, auto_refresh=False, screen=True) as live:
            while True:
                time.sleep(1 / fps)
                # frame += 1
                self.update()
                live.update(self.layout, refresh=True)
