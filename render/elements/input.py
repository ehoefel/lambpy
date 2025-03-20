from rich.style import Style
from rich.text import Text
from rich.panel import Panel
from render.window import Window


class Input(Window):

    def __init__(self, placeholder="", parser=None):
        super().__init__()
        self.placeholder = placeholder
        self.parser = parser
        self.value = ""
        self.cursor = 0
        self.style = ""
        # self.input_functions[27] = lambda: False
        self.input_functions[67] = lambda: self.move_cursor(1)
        self.input_functions[68] = lambda: self.move_cursor(-1)
        self.input_functions[91] = lambda: False
        self.input_functions[126] = lambda: self.delete()
        self.input_functions[127] = lambda: self.backspace()

    def delete(self):
        if len(self.value) == 0:
            return False

        if self.cursor == len(self.value):
            return False

        new_value = self.value[:self.cursor]
        new_value += self.value[self.cursor + 1:]

        self.value = new_value
        return True

    def backspace(self):
        if len(self.value) == 0:
            return False

        if self.cursor == 0:
            return False

        new_value = self.value[:self.cursor - 1]
        new_value += self.value[self.cursor:]

        self.value = new_value
        self.cursor -= 1
        return True

    def move_cursor(self, amount):
        new_cursor = self.cursor + amount
        if new_cursor < 0:
            return False
        if new_cursor > len(self.value):
            return False

        self.cursor = new_cursor

        return True

    def input(self, char):
        import string
        r = super().input(char)
        if r is not None:
            return r

        if char not in string.printable:
            return False

        if self.parser:
            char = self.parser(char)

        if char == '\\':
            char = 'λ'
        new_value = self.value[:self.cursor]
        new_value += char
        new_value += self.value[self.cursor + 1:]

        self.value = new_value
        self.cursor += 1
        return True

    def render(self, focused):

        style = self.style
        padding = (0, 1)
        if not focused:
            style += " dim"

        text = self.value
        text_empty = len(text) == 0
        if text_empty:
            text = Text(self.placeholder, "italic dim")

        cursor_style = Style(dim=True, italic=True, color="green")
        if text_empty:
            if focused:
                cursor_str = Text("🮇", style=cursor_style)
                text = Text.assemble(cursor_str, text)
                padding = (0, 0)
        elif focused:
            text_before = text[:self.cursor]
            text_after = text[self.cursor:]
            if self.cursor == len(text):
                cursor_str = Text("▎", style=cursor_style)
                text = Text.assemble(text, cursor_str)
            else:
                text_before = text[:self.cursor]
                text_after = text[self.cursor + 1:]

                cursor_style = Style(bgcolor="dark_green")
                cursor_char = Text(text[self.cursor], style=cursor_style)
                text = Text.assemble(text_before, cursor_char, text_after)
        else:
            pass

        return Panel(text, style=style, border_style=style, padding=padding)
