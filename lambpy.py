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


def my_exit():
    term_any_key()
    exit()


input_functions = {
    4: lambda: my_exit(),
    10: lambda: my_exit()  # ENTER
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
        "right": "save"
    },
    "save": {
        "up": "input",
        "left": "next"
    }
}


class Next(Button):

    def __init__(self):
        super().__init__("Next Step", "white")


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


class DerivationInput(Input):

    def __init__(self):
        def parser(char):
            if char == '\\':
                char = 'λ'
            return char

        super().__init__(placeholder="(λx.x) a", parser=parser)



def update():
    global input_reader
    input_reader()


if __name__ == "__main__":
    input_reader = InputReader()
    body = Body()
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
    log = Log()
    log.log("SUCC ZERO", "δ")
    log.log("(λn.λf.λx.f (n f x)) ZERO", "β")
    log.log("λf.λx.f (ZERO f x)", "δ")
    log.log("λf.λx.f ((λf.λx.x) f x)", "β")
    log.log("λf.λx.f ((λx.x) x)", "β")
    log.log("λf.λx.f x")
    body.add("output", log)

    body.focus = "input"

    input_reader.on_read(body.input)

    renderer = Renderer()
    renderer.layout_update(body.update_layout)
    renderer.on_update(update)

    renderer()
