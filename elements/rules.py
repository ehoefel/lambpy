from textual.widget import Widget
from textual.widgets import ListView, ListItem, Label
from language.aux_functions import to_str
from textual.reactive import reactive


class Rule(Widget):

    def __init__(self, name, value):
        super().__init__()
        self.rule_name = name
        self.value = value

    def render(self):
        return "%s = %s" % (self.rule_name, to_str(self.value.expression))


class RuleList(Widget):

    rules_reactive = reactive("", recompose=True)

    def __init__(self, rules):
        super().__init__(id="rules")
        self.rules = rules
        self.update()

    def update(self):
        self.rules_reactive = str(self.rules)
        print("update", self.rules_reactive)

    def compose(self):
        yield Label("Rules")

        if len(self.rules) > 0:
            yield ListView(
                ListItem(*[Rule(name, exp) for name, exp in self.rules])
            )
        else:
            yield ListView()
