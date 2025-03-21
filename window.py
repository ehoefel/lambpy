from rich import box
from rich.panel import Panel
from rich.style import Style
from rich.text import Text


class Body:

    def __init__(self):
        self.focus = None
        self.elements = {}
        self.input_functions = {
            65: lambda: self.move_focus("up"),
            66: lambda: self.move_focus("down"),
            67: lambda: self.move_focus("right"),
            68: lambda: self.move_focus("left")
        }

    def move_focus(self, direction):
        if direction in self.focus_map[self.focus].keys():
            next_focus = self.focus_map[self.focus][direction]
            self.focus = next_focus

    def set_focus_map(self, focus_map):
        self.focus_map = focus_map

    def add_input_functions(self, functions):
        for key, function in functions.items():
            self.input_functions[key] = function

    def add(self, name, element):

        def render():
            if self.focus is not None:
                focused = element == self.elements[self.focus]
            else:
                focused = False

            return element.render(focused)

        element.on_render(render)
        self.elements[name] = element

    def update_layout(self, layout):
        for key, element in self.elements.items():
            layout[key].update(element)

    def input(self, char):
        if len(char) == 0:
            return

        if self.focus is not None:
            focused = self.elements[self.focus]
            success = focused.input(char)
            if success:
                return

        sign = ord(char)
        if sign in self.input_functions.keys():
            return self.input_functions[sign]()


class Window:

    def __init__(self):
        self.input_functions = {
            65: lambda: False,
            66: lambda: False,
            67: lambda: False,
            68: lambda: False
        }

    def input(self, char):
        sign = ord(char)
        if sign in self.input_functions.keys():
            return self.input_functions[sign]()
        return None

    def on_render(self, render_fn):
        self.render_fn = render_fn

    def render(self, focused):
        pass

    def __rich__(self):
        return self.render_fn()

