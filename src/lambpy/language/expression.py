
def can_bind(exp, variable, rebind=None):
    if not isinstance(exp, Variable):
        return False
    if exp.symbol != variable.symbol:
        return False
    if exp.binding != rebind:
        return False
    return True


def bind(exp, variable, rebind=None):
    if type(exp) == Application:
        if can_bind(exp.exp1, variable, rebind):
            exp.exp1 = variable
        else:
            bind(exp.exp1, variable, rebind)

        if can_bind(exp.exp2, variable, rebind):
            exp.exp2 = variable
        else:
            bind(exp.exp2, variable, rebind)

    elif type(exp) != Variable:
        if can_bind(exp.expression, variable, rebind):
            exp.expression = variable
        else:
            bind(exp.expression, variable, rebind)


def min_exp(exp):
    if not isinstance(exp, Expression):
        return Expression(exp)

    if type(exp) not in [Expression, Value]:
        return exp

    if isinstance(exp.expression, Expression):
        return min_exp(exp.expression)

    return exp


class Expression:

    def __init__(self, expression):
        self.expression = expression


class Grouping(Expression):

    def __init__(self, expression):
        super().__init__(expression)


class Application(Expression):

    def __init__(self, exp1, exp2):
        super().__init__(None)
        self.exp1 = min_exp(exp1)
        if type(self.exp1) == Grouping:
            self.exp1 = self.exp1.expression
        self.exp2 = min_exp(exp2)


class Variable(Expression):

    def __init__(self, symbol, binding=None):
        super().__init__(None)
        self.symbol = symbol
        self.binding = binding

    def __eq__(self, other):
        return type(other) == Variable and self.binding == other.binding


class Abstraction(Expression):

    def __init__(self, variable, expression):
        super().__init__(expression)
        if isinstance(self.expression, Variable):
            self.expression = Expression(self.expression)

        self.variable = variable
        oldbind = variable.binding
        self.variable.binding = self

        bind(self.expression, self.variable, oldbind)


class Rule(Variable):

    def __init__(self, symbol, expression):
        super().__init__(symbol)
        self.expression = min_exp(expression)

    def __eq__(self, other):
        return type(other) == Rule and self.symbol == other.symbol


class Value(Expression):

    def __init__(self, variable, expression):
        super().__init__(expression)
        self.variable = variable
