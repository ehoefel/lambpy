from language.expression import bind
from language.parser import parse
from language.expression import Rule


class LambdaRules:

    def __init__(self):
        self._items = {}

    def add(self, name, expression):
        self._items[name] = Rule(name, parse(expression, rule_list=self))

    def apply(self, expression):
        for rule in self._items.values():
            bind(expression, rule)

    def __iter__(self):
        return iter(self._items.items())

    def __len__(self):
        return len(self._items)

    def items(self):
        return self._items.items()

    def __repr__(self):
        return ", ".join([str(x) for x in self._items.items()])
