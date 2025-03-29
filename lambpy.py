# δ
# β
# ∵
# λ

from input import InputReader, term_any_key
from language.execution import Execution
from language.aux_functions import to_str

from textual.app import App
from textual.containers import Horizontal, Vertical
from textual.widgets import Static, Button, ListView, Input
from elements.input_field import InputField

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename="log.txt", level=logging.DEBUG)


def my_exit():
    logger.debug("my_exit called")
    term_any_key()
    exit()


input_functions = {
    4: lambda: my_exit(),
}

cursor_map = {
    "input": {
        "up": "help",
        "down": "next",
        "right": "start"
    },
    "start": {
        "up": "help",
        "down": "next",
        "left": "input",
    },
    "help": {
        "right": "info",
        "down": "start",
        "left": "start",
    },
    "info": {
        "left": "help",
        "down": "start",
    },
    "next": {
        "up": "input",
        "right": "save",
        "disabled": {
            "down": "save"
        }
    },
    "save": {
        "up": "input",
        "left": "next"
    }
}


class Next(Button):

    def __init__(self):
        super().__init__("Next Step", "white", disabled_style="dim grey37")

        def on_enter():
            global curr_execution
            logger.debug("calling next execution")
            res = curr_execution()
            logger.debug("returned: " + str(res))
            if not self.is_enabled():
                body.set_focus("save")

        input_functions = {
            10: on_enter
        }
        self.add_input_functions(input_functions)

    def is_enabled(self):
        global curr_execution
        return curr_execution is not None and not curr_execution.is_complete()


class Help(Button):

    def __init__(self):
        super().__init__("？Help", "cyan")


class Save(Button):

    def __init__(self):
        super().__init__("Save", "gold1")

        def on_enter():
            pass


class Info(Button):

    def __init__(self):
        super().__init__("🛈  Info", "cyan")


class Start(Button):

    def __init__(self):
        super().__init__("Start", "yellow")


curr_execution = None


class Lambpy(App):
    CSS_PATH = "lambpy.tcss"
    AUTO_FOCUS = "#input"

    def compose(self):
        yield Horizontal(
            Static("λ", id="logo"),
            Static("Lambda Calculus", id="title"),
            Static("Calculator", id="subtitle"),
            Button("？Help", variant="success", id="help"),
            Button("🛈 Info", variant="primary", id="info"),
            id="header"
        )
        yield Horizontal(
            Vertical(
                Horizontal(
                    InputField(placeholder="(λx.x) a", id="input"),
                    Button("Run", variant="error", id="run"),
                    id="input_area"
                ),
                ListView(id="execlog"),
                Horizontal(
                    Button("Next", variant="primary", id="next"),
                    Button("Save", variant="warning", id="save"),
                    id="footer"
                ),
                id="body2"
            ),
            ListView(id="rules"),
            id="body"
        )
        # yield Vertical(
        #     Horizontal(
        #         Placeholder("logo", id="logo"),
        #         Vertical(
        #             Placeholder("title", id="title"),
        #             Placeholder("subtitle", id="subtitle"),
        #         ),
        #         id="header"
        #     ),
        #     Horizontal(
        #         Vertical(
        #             Horizontal(
        #                 Placeholder("input", id="input"),
        #                 Placeholder("run", id="run")
        #             ),
        #             Placeholder("log", id="log"),
        #             Horizontal(
        #                 Placeholder("next", id="next"),
        #                 Placeholder("save", id="save"),
        #                 id="footer"
        #             )
        #         ),
        #         Placeholder("rules", id="rules"),
        #     )
        # )
        # yield Footer()


if __name__ == "__main__":
    app = Lambpy()
    app.run()


# if __name__ == "__main__":
#     input_reader = InputReader()
#     body.add_input_functions(input_functions)
#     body.set_focus_map(cursor_map)
#
#     body.add("save", Save())
#     body.add("info", Info())
#     body.add("next", Next())
#     body.add("help", Help())
#     body.add("input", DerivationInput())
#     rewrites = List("Rewrite Rules")
#     rewrites.add("SUCC = λn.λf.λx.f (n f x)")
#     rewrites.add("ZERO = λf.λx.x")
#     body.add("rewrites", rewrites)
#     body.add("start", Start())
#     title = StaticText("[bold]Lambda Calculus[/] [dim]Calculator[/]")
#     body.add("title", title)
#     logo = StaticText("[bold green]λ[/]")
#     body.add("logo", logo)
#     body.add("footer_middle", StaticText(""))
#     body.add("output", execution_log)
#
#     body.focus = "input"
#
#     input_reader.on_read(body.input)
#
#     renderer = Renderer()
#     renderer.layout_update(body.update_layout)
#     renderer.on_update(update)
#
#     renderer()
