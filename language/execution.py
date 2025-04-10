from language.aux_functions import call, to_str, debug_repr
from language.parser import parse
from language.expression import Rule

exec_chain = []
last_exec = None
DONE = "done"


class Execution():

    def __init__(self, exp):
        self.first_exp = exp
        self.steps = [self.first_exp]
        self.last_exec = self.first_exp
        self.complete_exec_cache = None

    def is_complete(self):
        if self.complete_exec_cache is not None:
            return self.complete_exec_cache
        res = call(self.last_exec)
        self.complete_exec_cache = self.last_exec == res
        self.complete_exec_cache |= type(self.last_exec) == Rule
        self.next_exec_cache = res
        return self.complete_exec_cache

    def __repr__(self):
        return to_str(self.last_exec)

    def __call__(self):
        if self.is_complete():
            return False

        res = self.next_exec_cache
        self.steps.append(res)
        self.last_exec = res
        self.next_exec_cache = None
        self.complete_exec_cache = None
        return True

    def get_result(self):
        return self.last_exec

#     rule("TRUE", "λx.λy.x")
#     rule("FALSE", "λx.λy.y")
#     rule("AND", "λp.λq.p q p")
#     rule("OR", "λp.λq.p p q")
#     rule("NOT", "λp.p FALSE TRUE")
#     rule("SUCC", "λn.λf.λx.f(n f x)")
#     rule("0", "λf.λx.x")
#     rule("1", "λf.λx.f x")
#     rule("2", "λf.λx.f (f x)")
#     rule("ADD", "λm.λn.m SUCC n")
#     rule("MULT", "λm.λn.m (ADD n) 0")
#     rule("POWER", "λb.λe.e b")
#     rule("PRED", "λn.λf.λx.n (λg.λh.h (g f)) (λu.x) (λu.u)")
#     rule("SUB", "λm.λn.n PRED m")
#     rule("is0", "λn.n (λx.FALSE) TRUE")
#     rule("LEQ", "λm.λn.is0 (SUB m n)")
#     rule("PAIR", "λx.λy.λf.f x y")
#     rule("1st", "λp.p TRUE")
#     rule("2nd", "λp.p FALSE")
#
#     exp = parse("SUB (SUCC (SUCC 2)) 2")
#
#     #print_chain(exp)
