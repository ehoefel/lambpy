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
