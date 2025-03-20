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
