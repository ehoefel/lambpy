# δ
# β
# ∵
# λ

from language.parser import parse
from language.execution import Execution

from textual.app import App
from textual.containers import Horizontal, Vertical
from textual.widgets import Static, Button
from elements.input_field import InputField
from elements.reduction_steps import ReductionSteps
from elements.run_button import Run
from elements.next_button import Next
from elements.rules import RuleList
from language.rules import LambdaRules

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename="log.txt", level=logging.DEBUG)

rules = LambdaRules()
rules.add("TRUE", "λx.λy.x")
rules.add("FALSE", "λx.λy.y")


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
                    Next("Next", variant="primary", id="next"),
                    Button("Save", variant="warning", id="save"),
                    id="footer"
                ),
                id="body2"
            ),
            RuleList(rules=rules),
            id="body"
        )

    def on_mount(self):
        run = app.get_widget_by_id("run")
        run.disabled = True
        next = app.get_widget_by_id("next")
        next.disabled = True

    def on_lambda_exec(self, event):
        input = app.get_widget_by_id("input")
        reduction_steps = app.get_widget_by_id("reduction_steps")
        execution = Execution(input.value)
        reduction_steps.start(execution)
        input.clear()
        next = app.get_widget_by_id("next")
        next.disabled = False
        app.set_focus(next)

    def on_lambda_next(self, event):
        reduction_steps = app.get_widget_by_id("reduction_steps")
        reduction_steps.next_step()
        next = app.get_widget_by_id("next")
        next.disabled = reduction_steps.is_complete()

    def on_input_changed(self, event):
        input = event.input
        value = input.value
        el = parse(value, rule_list=rules)
        invalid = el is None
        run = app.get_widget_by_id("run")
        run.disabled = invalid


if __name__ == "__main__":
    app = Lambpy()

    app.run()
