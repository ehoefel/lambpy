# δ
# β
# ∵
# λ

from input import InputReader, term_any_key
from render.body import Body
from render.renderer import Renderer
from render.elements.input import Input
from render.elements.button import Button
from render.elements.static_text import StaticText
from render.elements.list import List
from render.elements.log import Log
from language.execution import Execution
from language.aux_functions import to_str

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


class Info(Button):

    def __init__(self):
        super().__init__("🛈  Info", "cyan")


class Start(Button):

    def __init__(self):
        super().__init__("Start", "yellow")


class ExecutionLog(Log):

    def __init__(self):
        super().__init__()
        self.execution = None

    def set_execution(self, execution):
        self.execution = execution
        self.entries = []

    def __rich_console__(self, console, options):
        entries = []
        if self.execution is not None:
            for step in self.execution.steps:
                entries.append((to_str(step), "b"))
        self.entries = entries
        return super().__rich_console__(console, options)
        self.entries = []


curr_execution = None
execution_log = ExecutionLog()
body = Body()


class DerivationInput(Input):

    def __init__(self):
        def parser(char):
            if char == '\\':
                char = 'λ'
            return char

        super().__init__(placeholder="(λx.x) a", parser=parser)

        def on_enter():
            global curr_execution, execution_log, body
            curr_execution = Execution(self.value)
            execution_log.set_execution(curr_execution)

            body.set_focus("next")
            self.clear()
            return True

        input_functions = {
            10: on_enter
        }
        self.add_input_functions(input_functions)


def update():
    global input_reader
    input_reader()


if __name__ == "__main__":
    input_reader = InputReader()
    body.add_input_functions(input_functions)
    body.set_focus_map(cursor_map)

    body.add("save", Save())
    body.add("info", Info())
    body.add("next", Next())
    body.add("help", Help())
    body.add("input", DerivationInput())
    rewrites = List("Rewrite Rules")
    rewrites.add("SUCC = λn.λf.λx.f (n f x)")
    rewrites.add("ZERO = λf.λx.x")
    body.add("rewrites", rewrites)
    body.add("start", Start())
    title = StaticText("[bold]Lambda Calculus[/] [dim]Calculator[/]")
    body.add("title", title)
    logo = StaticText("[bold green]λ[/]")
    body.add("logo", logo)
    body.add("footer_middle", StaticText(""))
    body.add("output", execution_log)

    body.focus = "input"

    input_reader.on_read(body.input)

    renderer = Renderer()
    renderer.layout_update(body.update_layout)
    renderer.on_update(update)

    renderer()
