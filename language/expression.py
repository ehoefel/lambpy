
def can_bind(expression, variable, rebind=None):
    if isinstance(expression, Expression):
        if isinstance(expression, Variable):
            if expression.binding == rebind:
                if expression.symbol == variable.symbol:
                    return True
    return False


def apply_exp_rec(exp, condition_fn, operation):
    if not isinstance(exp, Expression):
        return
    if condition_fn(exp):
        operation(exp)
    children = exp.get_children()
    for child in children:
        apply_exp_rec(child, condition_fn, operation)


def priority(exp, can_consume=False):
    if not isinstance(exp, Expression):
        return 0

    t = type(exp)

    if t in [Variable, Value]:
        return 0

    if t == Application:
        p1 = priority(exp.exp1, can_consume=exp.exp2 is not None)
        p2 = priority(exp.exp2)
        v = max(p1, p2)
        return v

    if t == Abstraction:
        return max(1 if can_consume else 0, priority(exp.expression))

    if t == Rule:
        return max(1, priority(exp.expression))

    if t == Expression:
        return priority(exp.expression)

    if t == Grouping:
        return priority(exp.expression)

    print("missing type rule", exp, t)
    exit()


class Expression:

    def __init__(self, expression):
        if isinstance(expression, Expression):
            expression = expression._min()

        self.expression = expression

    def get_children(self):
        return [self.expression]

    def _min(self):
        if type(self) not in [Expression, Value]:
            return self

        if isinstance(self.expression, Expression):
            el = self.expression._min()
            return el

        return self

    def bind(self, variable, rebind=None):
        if can_bind(self.expression, variable, rebind):
            self.expression = variable
        else:
            self.expression.bind(variable, rebind)

    def __repr__(self):
        return str(self.expression)

    def clone(self):
        if isinstance(self.expression, Expression):
            return Expression(self.expression.clone())

        return Expression(self.expression)

    def beta_apply(self, value):
        if isinstance(self.expression, Expression):
            clone = self.clone()

            if self.expression == value.variable:
                clone.expression = value.expression.clone()
            elif not isinstance(self.expression, Variable):
                clone.expression = clone.expression.beta_apply(value)
            return clone
        return self

    def pop(self):
        if type(self) != Expression:
            return self, None

        if isinstance(self.expression, Expression):
            return self.expression.pop()

        return self.expression, None

    def __call__(self):
        if not isinstance(self.expression, Expression):
            return self

        res = self.expression()
        if res == self.expression:
            return self

        clone = self.clone()
        clone.expression = res
        if (type(self) == Abstraction and
                type(res) == Abstraction and
                self.variable.symbol == res.variable.symbol):
            var = res.variable
            new_symbol = var.symbol[0] + str(int("0" + var.symbol[1:]) + 1)
            res.rename(new_symbol)

        return clone


class Grouping(Expression):

    def __init__(self, expression):
        super().__init__(expression)

    def __repr__(self):
        return "(%s)" % str(self.expression)

    def clone(self):
        return Grouping(self.expression.clone())


class Application(Expression):

    def __init__(self, exp1, exp2):
        super().__init__(None)
        self.exp1 = Expression(exp1)._min()
        if type(self.exp1) == Grouping:
            self.exp1 = self.exp1.expression
        self.exp2 = Expression(exp2)._min()

    def get_children(self):
        return [self.exp1, self.exp2]

    def bind(self, variable, rebind=None):
        if can_bind(self.exp1, variable, rebind):
            self.exp1 = variable
        else:
            self.exp1.bind(variable, rebind)

        if can_bind(self.exp2, variable, rebind):
            self.exp2 = variable
        else:
            self.exp2.bind(variable, rebind)

    def __repr__(self):
        repr1 = str(self.exp1)
        if type(self.exp1) == Abstraction:
            repr1 = "(%s)" % (repr1)
        repr2 = str(self.exp2)
        return "%s %s" % (repr1, repr2)

    def clone(self):
        return Application(self.exp1.clone(), self.exp2.clone())

    def beta_apply(self, value):
        exp1 = Expression(self.exp1).beta_apply(value)._min()
        exp2 = Expression(self.exp2).beta_apply(value)._min()

        if exp1 == self.exp1 and exp2 == self.exp2:
            return self

        return Application(exp1, exp2)

    def pop(self):
        return self.exp1.clone(), self.exp2.clone()

    def __call__(self):
        can_consume = self.exp2 is not None
        p1 = priority(self.exp1, can_consume=can_consume)
        p2 = priority(self.exp2)

        if p1 <= 0 and p2 <= 0:
            return self

        exp1 = self.exp1
        exp2 = self.exp2

        if p1 >= p2:
            if isinstance(self.exp1, Abstraction):
                target, rest = self.exp2.pop()

                result = self.exp1(target)._min()
                if type(result) == Grouping:
                    result = result.expression

                if rest is None:
                    return result

                exp1 = result
                exp2 = rest
            else:
                exp1 = exp1()
                exp2 = exp2.clone()
        else:
            exp1 = exp1.clone()
            exp2 = exp2()

        if type(exp1) == Variable and type(exp2) == Grouping:
            if type(exp2.expression) == Variable:
                exp2 = exp2.expression

        return Application(exp1, exp2)


class Variable(Expression):

    def __init__(self, symbol):
        super().__init__(None)
        self.symbol = symbol
        self.binding = None

    def bind(self, variable, rebind=None):
        return None

    def __repr__(self):
        return str(self.symbol)

    def clone(self):
        v = Variable(self.symbol)
        v.binding = self.binding
        return v

    def __eq__(self, other):
        return type(other) == Variable and self.binding == other.binding

    def rename(self, new_symbol):
        self.symbol = new_symbol


class Abstraction(Expression):

    def __init__(self, variable, expression, bind=True):
        super().__init__(expression)
        if isinstance(self.expression, Variable):
            self.expression = Expression(self.expression)

        self.variable = variable
        oldbind = variable.binding
        self.variable.binding = self

        if bind:
            self.expression.bind(self.variable, oldbind)

    def __repr__(self):
        return "λ%s.%s" % (str(self.variable), str(self.expression))

    def clone(self):
        exp = self.expression.clone()
        var = self.variable.clone()
        exp.bind(var, rebind=self.expression)
        return Abstraction(var, exp)

    def __call__(self, expression=None):
        if not expression:
            return super().__call__()

        value = Value(self.variable, expression)
        return self.expression.clone().beta_apply(value)

    def rename(self, new_symbol):
        condition = lambda exp: exp == self.variable
        operation = lambda exp: exp.rename(new_symbol)
        apply_exp_rec(self.expression, condition, operation)
        self.variable.symbol = new_symbol


class Rule(Variable):

    def __init__(self, symbol, expression):
        super().__init__(symbol)
        self.expression = Expression(expression)._min()

    def __call__(self):
        value = Value(self, self.expression)
        return value

    def clone(self):
        return Rule(self.symbol, self.expression.clone())


class Value(Expression):

    def __init__(self, variable, expression):
        super().__init__(expression)
        self.variable = variable

    def __repr__(self):
        return str(self.expression)

    def __call__(self):
        return self
