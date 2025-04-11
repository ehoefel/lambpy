from textual.widget import Widget
from textual.widgets import ListView, ListItem, Label, Static
from language.aux_functions import to_str
from textual.reactive import reactive
from textual.containers import Horizontal, Vertical


class Rule(Widget, can_focus=False):

    def __init__(self, name, value):
        super().__init__()
        self.rule_name = name
        self.value = value

    def compose(self):
        yield Horizontal(
            Label(self.rule_name, classes="name"),
            Label("=", classes="equals"),
            Label(to_str(self.value.expression), classes="value"),
        )


class RuleList(Static):

    rules_reactive = reactive("", recompose=True)

    def __init__(self, rules):
        super().__init__(id="rules")
        self.rules = rules
        self.update()

    def update(self):
        self.rules_reactive = str(self.rules)

    def compose(self):
        yield Label("Rules", classes="title")

        if len(self.rules) > 0:
            yield Vertical(
                *[Rule(name, exp) for name, exp in self.rules],
                classes="body"
            )
        else:
            yield ListView()
