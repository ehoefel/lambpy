from textual.widget import Widget
from textual.widgets import Label

from language import expression as langexp
from language.aux_functions import next_to_exec


def get_renderable(exp):
    if type(exp) == langexp.Expression:
        return Expression(exp)
    if type(exp) == langexp.Grouping:
        return Grouping(exp)
    if type(exp) == langexp.Application:
        return Application(exp)
    if type(exp) == langexp.Variable:
        return Variable(exp)
    if type(exp) == langexp.Abstraction:
        return Abstraction(exp)
    if type(exp) == langexp.Rule:
        return Rule(exp)
    return None


class Executable(Widget):

    def __init__(self, exp):
        super().__init__()
        self.exp = get_renderable(exp)
        nte = next_to_exec(exp)
        self.executable = None

        def highlight_nte(other):
            if self.executable is not None:
                return
            if other.literal == nte:
                self.executable = other
                other.set_executable()

        self.exp.walk(highlight_nte)

    def compose(self):
        yield self.exp
        operation = None
        if type(self.executable) == Rule:
            operation = Label("δ", classes="operation delta")
        if type(self.executable) == Application:
            operation = Label("β", classes="operation beta")

        if operation is not None:
            yield Label("∵", classes="therefore")
            yield operation


class Expression(Widget):

    def __init__(self, exp):
        super().__init__()
        self.literal = exp
        if type(self) == Expression:
            self.exp = get_renderable(self.literal.expression)

    def get_walkable(self):
        return [self.exp]

    def compose(self):
        yield self.exp

    def walk(self, fn):
        fn(self)
        for exp in self.get_walkable():
            exp.walk(fn)

    def set_executable(self):
        self.add_class("executable")


class Grouping(Expression):

    def __init__(self, exp):
        super().__init__(exp)
        self.exp = get_renderable(exp.expression)

    def compose(self):
        yield Label("(")
        yield self.exp
        yield Label(")")


class Application(Expression):

    def __init__(self, exp):
        super().__init__(exp)
        self.exp1 = get_renderable(exp.exp1)
        self.exp1.add_class("exp1")
        self.exp2 = get_renderable(exp.exp2)
        self.exp2.add_class("exp2")

    def get_walkable(self):
        return [self.exp1, self.exp2]

    def compose(self):
        el1 = [self.exp1]
        if type(self.exp1) == Abstraction:
            el1 = [Label("("), self.exp1, Label(")")]

        for e in el1:
            yield e
        yield Label(" ")
        yield self.exp2

    def set_executable(self):
        super().set_executable()
        self.exp1.set_executable()


class Variable(Expression):

    def __init__(self, exp):
        super().__init__(exp)

    def compose(self):
        yield Label(self.literal.symbol)

    def get_walkable(self):
        return []

    def set_executable(self):
        self.add_class("destination")


class Abstraction(Expression):

    def __init__(self, exp):
        super().__init__(exp)
        self.variable = get_renderable(exp.variable)
        self.variable.add_class("abs-var")
        self.exp = get_renderable(exp.expression)
        self.vars = []
        self.walk(lambda exp: self.assign_var(exp))

    def set_executable(self):
        super().set_executable()
        for var in self.vars:
            var.set_executable()

    def assign_var(self, exp):
        if type(exp) != Variable:
            return
        if self.literal.variable == exp.literal:
            self.vars.append(exp)

    def compose(self):
        yield Label("λ", classes="lambda")
        yield self.variable
        yield Label(".")
        yield self.exp


class Rule(Variable):

    def __init__(self, exp):
        super().__init__(exp)

    def compose(self):
        yield Label(self.literal.symbol)

    def set_executable(self):
        self.add_class("executable")
