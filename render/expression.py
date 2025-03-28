from language.aux_functions import depth_first
from language import expression


def to_str(exp, acc):
    if type(exp) == expression.Expression:
        return acc[0]
    if type(exp) == expression.Rule:
        return exp.symbol
    if type(exp) == expression.Variable:
        return exp.symbol
    if type(exp) == expression.Abstraction:
        return "!%s.%s" % (to_str(exp.variable), acc[0])
    if type(exp) == expression.Application:
        repr1 = acc[0]
        if type(exp.exp1) == expression.Abstraction:
            repr1 = "[%s]" % (repr1)

        repr2 = acc[1]

        return "%s %s" % (repr1, repr2)
    if type(exp) == expression.Grouping:
        return "{%s}" % acc[0]


if __name__ == "__main__":
    from ..language.parser import rule, parse
    rule("2", "λf.λx.f (f x)")
    exp = parse("SUB (SUCC (SUCC 2)) 2")
    print("hello")
    print(depth_first(exp, to_str))
