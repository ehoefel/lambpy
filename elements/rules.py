from textual.widget import Widget
from textual.widgets import ListView, ListItem, Label
from language.aux_functions import to_str


class Rule(Widget):

    def __init__(self, name, value):
        super().__init__()
        self.rule_name = name
        self.value = value

    def render(self):
        return "%s = %s" % (self.rule_name, to_str(self.value.expression))


class RuleList(Widget):

    def __init__(self, rules):
        super().__init__(id="rules")
        self.rules = rules

    def compose(self):
        yield Label("Rules")

        yield ListView(
            ListItem(*[Rule(name, exp) for name, exp in self.rules])
        )
