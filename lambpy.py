# δ
# β
# ∵
# λ

from language.parser import parse
from language.execution import Execution
from language.aux_functions import to_str

from textual.app import App
from textual.containers import Horizontal, Vertical
from textual.widgets import Static, Button
from elements.input_field import InputField
from elements.reduction_steps import ReductionSteps
from elements.run_button import Run
from elements.next_button import Next
from elements.save_button import Save
from elements.rules import RuleList
from elements.modal import SaveModal
from language.rules import LambdaRules

import argparse
import pathlib

rules = LambdaRules()


class Lambpy(App):
    CSS_PATH = "css/lambpy.tcss"
    AUTO_FOCUS = "#input_exp_run"

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
                    InputField(placeholder="(λx.x) a", id="input_exp_run"),
                    Run("Run", variant="error", id="run"),
                    id="input_area"
                ),
                ReductionSteps(id="reduction_steps"),
                Horizontal(
                    Next("Next", variant="primary", id="next"),
                    Save("Save", variant="warning", id="save"),
                    id="footer"
                ),
                id="body2"
            ),
            RuleList(rules=rules),
            id="body"
        )

    def on_mount(self):
        if self.screen != self.default_screen:
            return
        run = app.get_widget_by_id("run")
        run.disabled = True
        next = app.get_widget_by_id("next")
        next.disabled = True
        save = app.get_widget_by_id("save")
        save.disabled = True

    def on_lambda_exec(self, event):
        if self.screen != self.default_screen:
            return
        run = app.get_widget_by_id("run")
        if run.disabled:
            return

        input = app.get_widget_by_id("input_exp_run")
        reduction_steps = app.get_widget_by_id("reduction_steps")
        exp = parse(input.value, rule_list=rules)
        execution = Execution(exp)
        reduction_steps.start(execution)
        input.clear()
        next = app.get_widget_by_id("next")
        next.disabled = False
        app.set_focus(next)
        next.disabled = reduction_steps.is_complete()
        save = app.get_widget_by_id("save")
        save.disabled = False
        if next.disabled:
            app.set_focus(save)

    def on_lambda_next(self, event):
        if self.screen != self.default_screen:
            return
        reduction_steps = app.get_widget_by_id("reduction_steps")
        reduction_steps.next_step()
        next = app.get_widget_by_id("next")
        next.disabled = reduction_steps.is_complete()

    def on_lambda_save(self, event):
        if self.screen != self.default_screen:
            return
        reduction_steps = app.get_widget_by_id("reduction_steps")
        el = reduction_steps.get_last_step()
        self.push_screen(SaveModal(to_str(el)))

    def on_input_changed(self, event):
        if self.screen != self.default_screen:
            return
        input = event.input
        run = app.get_widget_by_id("run")
        run.disabled = not input.is_valid

    def on_save_rule(self, event):
        global rules
        rules.add(event.name, event.expression)
        rule_list = app.get_widget_by_id("rules")
        rule_list.update()
        app.set_focus(app.get_widget_by_id("input_exp_run"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="lambpy",
        description="Lambda Calculus interpreter in Python"
    )
    parser.add_argument("-r", "--rules", type=pathlib.Path)
    args = parser.parse_args()
    app = Lambpy()
    if args.rules is not None:
        try:
            with open(args.rules) as fp:
                for line in fp:
                    line = line.rstrip()
                    name, exp = line.split("=")
                    name = name.lstrip().rstrip()
                    exp = exp.lstrip().rstrip()
                    rules.add(name, exp)
        except FileNotFoundError:
            parser.print_usage()
            exit()

    app.run()
