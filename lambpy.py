# δ
# β
# ∵
# λ

from language.execution import Execution
from language.parser import parse
from language.aux_functions import to_str

from textual.app import App
from textual.containers import Horizontal, Vertical
from textual.widgets import Static, Button, ListView
from elements.input_field import InputField
from elements.reduction_steps import ReductionSteps
from elements.run_button import Run

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename="log.txt", level=logging.DEBUG)


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
                    Run("Run", variant="error", id="run"),
                    id="input_area"
                ),
                ReductionSteps(id="reduction_steps"),
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

    def on_mount(self):
        run = app.get_widget_by_id("run")
        run.disabled = True

    def on_lambda_exec(self, event):
        input = app.get_widget_by_id("input")
        reduction_steps = app.get_widget_by_id("reduction_steps")
        reduction_steps.add_step(input.value)
        input.clear()
        next = app.get_widget_by_id("next")
        app.set_focus(next)

    def on_input_changed(self, event):
        input = event.input
        value = input.value
        el = parse(value)
        invalid = el is None
        print(el, type(el), invalid)
        run = app.get_widget_by_id("run")
        run.disabled = invalid



if __name__ == "__main__":
    app = Lambpy()

    app.run()
