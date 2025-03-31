from textual.binding import Binding
from textual.widgets import Input

from elements.messages import LambdaExec


class InputField(Input):

    BINDINGS = [
        Binding("\\", "lambda", "", priority=True, show=False, system=True)
    ]

    def action_lambda(self):
        self.insert_text_at_cursor("λ")

    def action_submit(self):
        self.post_message(LambdaExec())
