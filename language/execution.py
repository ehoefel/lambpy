
exec_chain = []
last_exec = None
DONE = "done"


def exec_next(exp):
    global exec_chain, last_exec
    if len(exec_chain) == 0 or exec_chain[0] != exp:
        exec_chain.clear()
        last_exec = exp
        exec_chain.append(exp)
        return exp

    if last_exec == DONE:
        return None

    res = last_exec()
    if last_exec == res:
        res = DONE
        exec_chain.append(res)
        return None

    exec_chain.append(res)
    last_exec = res
    return res


def get_final(exp):
    _ = exec_next(exp)
    while exec_chain[-1] != DONE:
        exec_next(exp)
    return exec_chain[-2]


def print_chain(exp):
    get_final(exp)
    for step in exec_chain:
        if step != DONE:
            print(step)


if __name__ == "__main__":
    from parser import rule, parse

    rule("TRUE", "λx.λy.x")
    rule("FALSE", "λx.λy.y")
    rule("AND", "λp.λq.p q p")
    rule("OR", "λp.λq.p p q")
    rule("NOT", "λp.p FALSE TRUE")
    rule("SUCC", "λn.λf.λx.f(n f x)")
    rule("0", "λf.λx.x")
    rule("1", "λf.λx.f x")
    rule("2", "λf.λx.f (f x)")
    rule("ADD", "λm.λn.m SUCC n")
    rule("MULT", "λm.λn.m (ADD n) 0")
    rule("POWER", "λb.λe.e b")
    rule("PRED", "λn.λf.λx.n (λg.λh.h (g f)) (λu.x) (λu.u)")
    rule("SUB", "λm.λn.n PRED m")
    rule("is0", "λn.n (λx.FALSE) TRUE")
    rule("LEQ", "λm.λn.is0 (SUB m n)")
    rule("PAIR", "λx.λy.λf.f x y")
    rule("1st", "λp.p TRUE")
    rule("2nd", "λp.p FALSE")

    exp = parse("2nd (PAIR 2 1)")

    # print(get_final(exp))
    print_chain(exp)
    # import code
    # code.interact(local=locals())
