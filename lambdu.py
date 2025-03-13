
PRETTY = False

def get_source(fn):
    from inspect import getsource
    if not callable(fn):
        return str(fn)

    source = getsource(fn)
    split = source.split("Lambda(")
    cb = split[0].count("(")
    cb2 = split[1].count("(")
    cb3 = split[1].count(")")

    rb = cb + cb2 - cb3

    source = getsource(fn).split("Lambda(")[1].rstrip()
    source = source[:rb]

    return source


class FGColor:
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    VIOLET = 35
    BEIGE = 36
    WHITE = 37
    BLACK2 = 90
    RED2 = 91
    GREEN2 = 92
    YELLOW2 = 93
    BLUE2 = 94
    VIOLET2 = 95
    BEIGE2 = 96
    WHITE2 = 97


class BGColor:
    BLACK = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    VIOLET = 45
    BEIGE = 46
    WHITE = 47
    BLACK2 = 100
    RED2 = 101
    GREEN2 = 102
    YELLOW2 = 103
    BLUE2 = 104
    VIOLET2 = 105
    BEIGE2 = 106
    WHITE2 = 107


class Style:
    NORMAL = 0
    BOLD = 1
    ITALIC = 3
    UNDERSCORE = 4
    BLINK = 5
    SELECT = 7


class Format:

    def __init__(self, style, fg, bg):
        self.style = style
        self.fg = fg
        self.bg = bg

    def __add__(self, other):
        style = max(self.style, other.style)
        fg = max(self.fg, other.fg)
        bg = max(self.bg, other.bg)
        return Format(style, fg, bg)

    def __call__(self, text):
        global PRETTY
        if not PRETTY:
            return text
        s = ";".join([str(self.style), str(self.fg), str(self.bg)])
        return "\x1b[%sm%s\x1b[0m" % (s, text)


Format.NAME = Format(Style.NORMAL, FGColor.YELLOW, BGColor.BLACK)
Format.EXPAND = Format(Style.BOLD, FGColor.YELLOW2, BGColor.BLACK)
Format.EXPANDED = Format(Style.NORMAL, FGColor.YELLOW2, BGColor.BLACK)
Format.CONSUME_IN = Format(Style.BOLD, FGColor.BLUE, BGColor.BLACK)
Format.CONSUME_PARAM = Format(Style.UNDERSCORE, FGColor.BLUE, BGColor.BLACK)
Format.CONSUME_OUT = Format(Style.SELECT, FGColor.BLUE, BGColor.BLACK)
Format.CONSUMED = Format(Style.NORMAL, FGColor.BLUE2, BGColor.BLACK)


def lambda_break(s):
    varname = s[s.index(".") - 1]
    full_varname = s[:s.index(".")]
    rest = s[s.index("."):]
    return (full_varname, varname, rest)


def pretty_lambda(s):
    global PRETTY
    if not hasattr(s, "step") or s.step is None:
        if s.name:
            if hasattr(s, "next_step") and s.next_step == "expand":
                return Format.EXPAND(s.name)
            return Format.NAME(s.name)
        else:
            return s.calc_fullname()

    step = s.step

    if step == "expand":
        return Format.EXPANDED(s.fullname)
    if step == "prepare":
        f, v, r = lambda_break(s.fullname)
        t = Format.CONSUME_IN(f) + r.replace(v, Format.CONSUME_OUT(v))
        PRETTY = False
        target = str(s.target)
        PRETTY = True
        return t + " " + Format.CONSUME_PARAM(target)
    if step == "execute":
        f, v, r = lambda_break(s.calc_fullname())
        PRETTY = False
        target = str(s.target)
        PRETTY = True
        return r[1:].replace(v, Format.CONSUMED(target))
    if step == "recursion":
        return s.calc_fullname()


def pretty(s):
    if type(s) == Lambda:
        return pretty_lambda(s)
    print(s, type(s))
    exit()


class Tape():

    def __init__(self, *items):
        self.items = list(items)

    def __or__(self, other):
        return Tape(*self.items, other)

    def __repr__(self):
        return " ".join([str(item) for item in self.items])

    @classmethod
    def clone(cls, tape):
        items = [item for item in tape.items]
        return Tape(*items)

    def __call__(self):
        from inspect import stack, getmodule
        global PRETTY

        frm = stack()[1]
        mod = getmodule(frm[0]).__name__

        if len(self.items) == 0:
            return self

        f = self.items.pop(0)
        if mod != "__main__":
            if not callable(f):
                return f

            f = f(self)

            if type(f) == Lambda or type(f) == Tape:
                return f | self

            return f

        str_print = None
        while True:
            try:
                f = f(self)
                if type(f) == tuple:
                    self.items = list(f)
                    f = self.items.pop(0)
                    f = f(self)

                if f.is_end(self):
                    break

                if str_print is not None:
                    print(str_print)

                PRETTY = True
                str_print = "%s %s" % (str(f), (str(self)))
                PRETTY = False

            except EOFError:
                print("exception end")
                break

        print()
        return f

    def pop(self):
        return self.items.pop(0)

    def __len__(self):
        return len(self.items)


class Lambda():

    def __init__(self, f, args=None, body=None, name=None):
        from inspect import signature, stack
        if name is None:
            frameinfo = stack()[1]
            code_context = frameinfo.code_context[0]
            self.name = code_context.split("Lambda")[0].rstrip(" =")
        else:
            self.name = name

        if args is None:
            args = list(signature(f).parameters)

        self.args = args
        if body is None:
            body_str = get_source(f).split(": ")[1]
            values = {value: value for index, value in enumerate(self.args)}
            body = eval(body_str, values)
            del body_str
            del values

        self.body = body
        self.fullname = self.calc_fullname()

        self.make_function()

    def calc_fullname(self):
        def rec(items):
            res = []
            if type(items) == str:
                return items
            for item in items:
                s = str(item)
                if type(item) == tuple:
                    s = "(%s)" % rec(item)
                if type(item) == Tape:
                    s = "(%s)" % s
                res.append(s)
            return " ".join(res)

        s_body = rec(self.body)

        return "".join(["λ%s." % arg for arg in self.args]) + s_body


    @classmethod
    def partial(cls, args, body):
        return Lambda(None, args=args, body=body, name=False)

    def make_function(self):
        def replace(items, var, value):
            if type(items) != tuple:
                if items == var:
                    return value
                return items

            new_items = []

            for index in range(len(items)):
                item = items[index]
                new_item = items[index]
                if var == item:
                    new_item = value
                if type(item) == tuple:
                    new_item = replace(item, var, value)
                new_items.append(new_item)
            return tuple(new_items)

        self.f = lambda x: replace(self.body, self.args[0], x)

    def __repr__(self):
        global PRETTY
        if PRETTY:
            return pretty(self)

        if self.name:
            return self.name
        else:
            return self.fullname

    def __or__(self, other):
        if type(other) == Tape:
            return Tape(self, *other.items)

        if type(other) == tuple:
            return Tape(self, *other)

        return Tape(self, other)

    def is_end(self, tape):
        stack = []
        tape = Tape.clone(tape)
        el = self

        def same(a, b):
            if type(a) != type(b):
                return False
            if str(a) != str(b):
                return False
            return True

        while same(self, el):
            try:
                el = el(tape)
                stack.append(el)
            except EOFError:
                return True
        return False

    def __call__(self, tape):
        self = Lambda.clone(self)

        if not hasattr(self, "step"):
            self.step = None

        if hasattr(self, "next_step"):
            self.step = self.next_step

        if self.step is None:
            if self.name:
                if len(tape) == 0:
                    raise EOFError
                self.next_step = "expand"
            else:
                if len(tape) == 0:
                    self.next_step = "recursion"
                else:
                    self.next_step = "prepare"
            return self

        if self.step == "expand":
            if len(tape) == 0:
                self.next_step = "recursion"
                return self

            self.next_step = "prepare"
            return self

        if self.step == "prepare":
            self.target = tape.pop()
            self.next_step = "execute"
            return self

        if self.step == "execute":
            self.next_step = "execute2"
            return self

        if self.step == "execute2":
            res_body = self.f(self.target)
            if type(res_body) != tuple:
                res_body = (res_body,)
            res_args = self.args[1:]
            if len(res_args) > 0:
                return Lambda.partial(args=res_args, body=res_body)(tape)(tape)

            if len(res_body) == 1:
                res_body = res_body[0]
            return res_body

        if self.step == "recursion":

            def exec_rec(body):
                new_body = []
                step = False
                for b in body:
                    if type(b) == tuple:
                        b = Tape(*b)()
                    if callable(b) and not step:
                        b = b()
                        step = True
                    new_body.append(b)
                if not step:
                    raise EOFError()
                return tuple(new_body)

            self.body = exec_rec(self.body)
            self.fullname = self.calc_fullname()
            return self

    @classmethod
    def clone(cls, self):
        from copy import deepcopy
        f = self.f
        args = self.args.copy()
        body = deepcopy(self.body)
        name = self.name

        clone = Lambda(f, args, body, name)

        if hasattr(self, "step"):
            clone.step = self.step
        if hasattr(self, "next_step"):
            clone.next_step = self.next_step
        if hasattr(self, "target"):
            clone.target = self.target

        return clone
