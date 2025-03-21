from language.aux_functions import depth_first, call, next_exec, to_str
from language import expression
from rich import print


next_exec_exp = []


def render(exp, acc):
    if not isinstance(exp, expression.Expression):
        return str(exp)

    def abstraction_render():
        ltext = "λ"
        vtext = "%s" % (exp.variable.symbol)
        dtext = "."
        rtext = "%s" % (acc[0])
        a = ltext + vtext + dtext + rtext
        return a

    def application_render():
        repr1 = acc[0]
        repr2 = acc[1]
        if type(exp.exp1) == expression.Abstraction:
            "(%s)" % (repr2)

        return "%s %s" % (repr1, repr2)

    map = {
        expression.Expression: lambda: acc[0],
        expression.Rule: lambda: "[yellow]%s[/]" % (exp.symbol),
        expression.Variable: lambda: "%s" % (exp.symbol),
        expression.Abstraction: abstraction_render,
        expression.Application: application_render,
        expression.Grouping: lambda: "[dim]([/]%s[dim])[/]" % (acc[0])
    }
    res = map[type(exp)]()
    global next_exec_exp
    if type(exp) in [expression.Rule, expression.Abstraction]:
        if exp in next_exec_exp:
            pass
            # res = "[bold]%s[/]" % (res)
        else:
            pass
            # res = "[dim]%s[/]" % (res)
    return res


def exp_print(exp):
    global next_exec_exp
    next_exec_exp.clear()
    next_exec_exp = next_exec(exp)

    print(depth_first(exp, render))


if __name__ == "__main__":
    from language.parser import rule, parse
    rule("PRED", "λn.λf.λx.n (λg.λh.h (g f)) (λu.x) (λu.u)")
    rule("2", "λf.λx.f (f x)")
    rule("SUCC", "λn.λf.λx.f(n f x)")
    rule("SUB", "λm.λn.n PRED m")
    exp = parse("SUB (SUCC (SUCC 2)) 2")
    exp_print(exp)
    exp2 = call(exp)
    exp_print(exp2)
