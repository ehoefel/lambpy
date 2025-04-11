from textual.widget import Widget
from textual.widgets import Label
from textual.containers import Horizontal

from language import expression as langexp
from language.aux_functions import can_exec


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

    class HoverStack():

        def __init__(self):
            self.list = []
            pass

        def clear_class(self):
            for other in self.list:
                other.remove_class("hover")

        def update_class(self):
            if len(self.list) == 0:
                return
            self.list[-1].add_class("hover")
            print(self.list)

        def set(self, stack):
            print("set", self.list, stack)
            if len(self.list) > len(stack):
                return
            self.clear_class()
            self.list = stack
            self.update_class()
            print("result", self.list)

        def remove(self, el):
            print("remove", self.list, el)
            if el in self.list:
                if el == self.list[-1]:
                    el.remove_class("hover")
                self.list.remove(el)
            self.update_class()
            print("result", self.list)

    def __init__(self, exp):
        super().__init__()
        self.exp = get_renderable(exp)
        self.hover_stack = Executable.HoverStack()

    def compose(self):
        yield self.exp

    def hover(self, stack):
        self.hover_stack.set(stack)

    def hover_off(self, el):
        self.hover_stack.remove(el)


class Expression(Widget):

    def __init__(self, exp):
        super().__init__()
        self.literal = exp
        if can_exec(self.literal):
            self.add_class("executable")

    def compose(self):
        if not hasattr(self, "exp"):
            self.exp = get_renderable(self.literal.expression)
        yield self.exp

    def hover(self, stack):
        self.parent.hover([self] + stack)

    def hover_off(self, el=None):
        if el is None:
            el = self
        self.parent.hover_off(el)


class Grouping(Expression):

    def __init__(self, exp):
        super().__init__(exp)
        self.exp = get_renderable(exp.expression)

    def compose(self):
        yield Horizontal(
            Label("("),
            self.exp,
            Label(")")
        )


class Application(Expression):

    def __init__(self, exp):
        super().__init__(exp)
        self.exp1 = get_renderable(exp.exp1)
        self.exp1.add_class("exp1")
        self.exp2 = get_renderable(exp.exp2)
        self.exp2.add_class("exp2")

    def compose(self):
        yield Horizontal(
            self.exp1,
            Label(" "),
            self.exp2
        )

    def on_enter(self, event):
        self.hover([])
        pass
        # self.root.hover_stack.add(self)
        # self.add_class("hover")

    def on_leave(self, event):
        self.hover_off()


class Variable(Expression):

    def __init__(self, exp):
        super().__init__(exp)

    def compose(self):
        yield Label(self.literal.symbol)


class Abstraction(Expression):

    def __init__(self, exp):
        super().__init__(exp)
        self.variable = get_renderable(exp.variable)
        self.exp = get_renderable(exp.expression)

    def compose(self):
        if not self.has_class("executable"):
            p = self.parent
            print(self, p, type(p))
            has_exec = False
            while not isinstance(p, Executable):
                print('checking', p)
                if p.has_class("executable"):
                    print('has class')
                    has_exec = True
                    break
                p = p.parent
            if not has_exec:
                self.add_class("nonexecutable")
        yield Horizontal(
            Label("λ"),
            self.variable,
            Label("."),
            self.exp
        )


class Rule(Variable):

    def __init__(self, exp):
        super().__init__(exp)

    def compose(self):
        yield Label(self.literal.symbol)

    def on_enter(self, event):
        self.hover([])

    def on_leave(self, event):
        self.hover_off()
        pass
