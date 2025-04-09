from textual.binding import Binding
from textual.widgets import Input

from elements.messages import LambdaExec
from textual.validation import Function
from language.parser import parse


def validate_parse(value):
    exp = parse(value)
    return exp is not None


class InputField(Input):

    BINDINGS = [
        Binding("\\", "lambda", "", priority=True, show=False, system=True)
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs, validators=[Function(validate_parse)])

    def action_lambda(self):
        self.insert_text_at_cursor("λ")

    def action_submit(self):
        self.post_message(LambdaExec())
