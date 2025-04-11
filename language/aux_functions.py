from language.expression import Expression, Grouping, Application, Abstraction
from language.expression import Variable, Rule, Value
from language.expression import min_exp, bind
import logging

logger = logging.getLogger(__name__)


def depth_first(exp, fn):
    if not isinstance(exp, Expression):
        return fn(exp, [])

    children = get_children(exp)
    acc = []
    for child in children:
        acc.append(depth_first(child, fn))

    return fn(exp, acc)


def get_children(exp):
    if type(exp) == Application:
        return (exp.exp1, exp.exp2)
    return (exp.expression,)


def apply_exp_rec(exp, condition_fn, operation):
    if not isinstance(exp, Expression):
        return
    if condition_fn(exp):
        operation(exp)
    children = get_children(exp)
    for child in children:
        apply_exp_rec(child, condition_fn, operation)


def can_exec(exp):
    if type(exp) == Application:
        return type(exp.exp1) == Abstraction
    if type(exp) == Rule:
        return True
    return False


def next_exec(exp):
    if not isinstance(exp, Expression):
        return []
    if type(exp) == Variable:
        return []
    if type(exp) in [Expression, Abstraction, Grouping]:
        nexp = next_exec(exp.expression)
        if len(nexp) > 0:
            return nexp + [exp]
        return []
    if type(exp) == Rule:
        return [exp]
    if type(exp) == Application:
        if type(exp.exp1) == Abstraction:
            return [exp.exp1, exp.exp1.variable, exp]
        nexp1 = next_exec(exp.exp1)
        if len(nexp1) > 0:
            return nexp1 + [exp]
        nexp2 = next_exec(exp.exp2)
        if len(nexp2) > 0:
            return nexp2 + [exp]
        return []


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


def to_str(exp):
    def abstraction_str(x):
        return "λ%s.%s" % (to_str(x.variable), to_str(x.expression))

    def application_str(x):
        repr1 = to_str(x.exp1)
        if type(x.exp1) == Abstraction:
            repr1 = "(%s)" % (repr1)

        return "%s %s" % (repr1, to_str(x.exp2))

    map = {
        Expression: lambda x: to_str(x.expression),
        Value: lambda x: to_str(x.expression),
        Rule: lambda x: str(x.symbol),
        Variable: lambda x: str(x.symbol),
        Abstraction: abstraction_str,
        Application: application_str,
        Grouping: lambda x: "(%s)" % (to_str(exp.expression)),
    }

    if type(exp) not in map.keys():
        return exp

    return map[type(exp)](exp)


def clone(exp):
    def clone_abstraction():
        exp2 = clone(exp.expression)
        var = clone(exp.variable)
        bind(exp2, var, rebind=exp.expression)
        return Abstraction(var, exp2)

    map = {
        Expression: lambda: Expression(clone(exp.expression)),
        Grouping: lambda: Grouping(clone(exp.expression)),
        Application: lambda: Application(clone(exp.exp1), clone(exp.exp2)),
        Variable: lambda: Variable(exp.symbol, exp.binding),
        Rule: lambda: Rule(exp.symbol, clone(exp.expression)),
        Abstraction: clone_abstraction
    }

    return map[type(exp)]()


def pop(exp):
    if type(exp) == Application:
        return clone(exp.exp1), clone(exp.exp2)

    if type(exp) != Expression:
        return exp, None

    return pop(exp.expression)


def application_call(exp, target=None):
    can_consume = exp.exp2 is not None
    p1 = priority(exp.exp1, can_consume=can_consume)
    p2 = priority(exp.exp2)

    if p1 <= 0 and p2 <= 0:
        return exp

    exp1 = exp.exp1
    exp2 = exp.exp2

    if p1 >= p2:
        if isinstance(exp.exp1, Abstraction):
            target, rest = pop(exp.exp2)

            result = min_exp(call(exp.exp1, target))
            if type(result) == Grouping:
                result = result.expression

            if rest is None:
                return result

            exp1 = result
            exp2 = rest
        else:
            exp1 = call(exp1)
            exp2 = clone(exp2)
    else:
        exp1 = clone(exp1)
        exp2 = call(exp2)

    if type(exp1) == Variable and type(exp2) == Grouping:
        if type(exp2.expression) == Variable:
            exp2 = exp2.expression

    return Application(exp1, exp2)


def abstraction_call(exp, target=None):
    if target is None:
        res = call(exp.expression)
        if res == exp.expression:
            return exp

        if type(res) == Abstraction:
            if exp.variable.symbol == res.variable.symbol:
                var = res.variable
                new_symbol = var.symbol[0] + str(int("0" + var.symbol[1:]) + 1)
                rename(res, new_symbol)

        c = clone(exp)
        c.expression = res
        return c
    return beta_apply(clone(exp.expression), Value(exp.variable, target))


def expression_call(exp, target=None):
    res = call(exp.expression)
    if res == exp.expression:
        return exp

    c = clone(exp)
    c.expression = res

    return c


def debug_repr(exp):
    def abstraction_str(x):
        return "<Abs[%s].%s>" % (to_str(x.variable), debug_repr(x.expression))

    def application_str(x):
        repr1 = debug_repr(x.exp1)

        return "<App [%s] [%s]>" % (repr1, debug_repr(x.exp2))

    map = {
        Expression: lambda x: "<Exp [%s]>" % (debug_repr(x.expression)),
        Value: lambda x: "<Value [%s]>" % (debug_repr(x.expression)),
        Rule: lambda x: "<Rule [%s] [%s]>" % (str(x.symbol), to_str(x.expression)),
        Variable: lambda x: "<Var [%s]>" % (str(x.symbol)),
        Abstraction: abstraction_str,
        Application: application_str,
        Grouping: lambda x: "<Group [%s]>" % (debug_repr(exp.expression)),
    }

    if type(exp) not in map.keys():
        return exp

    return map[type(exp)](exp)


def call(exp, target=None):
    map = {
        Application: application_call,
        Abstraction: abstraction_call,
        Rule: lambda x, y: x.expression,
        Expression: expression_call,
        Grouping: expression_call
    }
    key = type(exp)
    if key in map.keys():
        return map[key](exp, target)

    return exp


def rename(exp, new_symbol):
    if isinstance(exp, Abstraction):
        condition = lambda other: other == exp.variable
        operation = lambda other: rename(other, new_symbol)
        apply_exp_rec(exp.expression, condition, operation)
        exp.variable.symbol = new_symbol
    if isinstance(exp, Variable):
        exp.symbol = new_symbol


def beta_apply(exp, value):
    if isinstance(exp, Application):
        exp1 = min_exp(beta_apply(Expression(exp.exp1), value))
        exp2 = min_exp(beta_apply(Expression(exp.exp2), value))

        if exp1 == exp.exp1 and exp2 == exp.exp2:
            return exp

        return Application(exp1, exp2)

    c = clone(exp)

    if exp.expression == value.variable:
        c.expression = clone(value.expression)
        if type(c) == Expression:
            c = c.expression
    elif not isinstance(exp.expression, Variable):
        c.expression = beta_apply(c.expression, value)
        if isinstance(c, Abstraction):
            if isinstance(c.expression, Grouping):
                c.expression = c.expression.expression
    return c
