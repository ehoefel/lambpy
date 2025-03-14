
PRETTY = False

KNOWN_NAMES = {}


def print_tree(obj):
    if type(obj) == tuple:
        return "tuple[%s]" % (", ".join([print_tree(el) for el in obj]))
    if type(obj) == Tape:
        return "Tape[%s]" % (", ".join([print_tree(el) for el in obj.items]))
    if type(obj) == Abstraction:
        step = obj.step if hasattr(obj, "step") else None
        body = ", ".join([print_tree(el) for el in obj.body])
        return "Abstraction(%s)%s[%s]" % (step, obj.args, body)
    return "%s[%s]" % (type(obj), str(obj))


def is_final(el):
    if type(el) == tuple:
        for el2 in el:
            if not is_final(el2):
                return False
        return True
    if type(el) == Tape:
        return is_final(tuple(el.items))
    if type(el) == Abstraction:
        if not hasattr(el, "step"):
            return False
        return el.step == "recursion" and is_final(el.body)
    return True


def get_source(fn):
    from inspect import getsource
    if not callable(fn):
        return str(fn)

    source = getsource(fn)
    split = source.split("Abstraction(")
    cb = split[0].count("(")
    cb2 = split[1].count("(")
    cb3 = split[1].count(")")

    rb = cb + cb2 - cb3

    source = getsource(fn).split("Abstraction(")[1].rstrip()
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
    # print("rendering ", step)

    if step == "expand":
        old_pretty = PRETTY
        PRETTY = False
        fullname = s.calc_fullname()
        PRETTY = old_pretty
        return Format.EXPANDED(fullname)
    if step == "prepare":
        f, v, r = lambda_break(s.calc_fullname())
        q = r.replace("." + v, "." + Format.CONSUME_OUT(v))
        q = q.replace(" " + v, " " + Format.CONSUME_OUT(v))
        t = Format.CONSUME_IN(f) + q
        old_pretty = PRETTY
        PRETTY = False
        target = str(s.target)
        PRETTY = old_pretty
        return t + " " + Format.CONSUME_PARAM(target)
    if step == "execute":
        f, v, r = lambda_break(s.calc_fullname())
        if len(s.args) == 1 and r[0] == "(":
            first = str(s.body[0])
            r = r.replace("(%s)" % first, first)
        old_pretty = PRETTY
        PRETTY = False
        target = str(s.target)
        PRETTY = old_pretty
        if target[0] == "λ":
            r = r.replace("." + v, ".(%s)" % (v))
        q = r.replace("." + v, "." + Format.CONSUMED(target))
        q = q.replace(" " + v, " " + Format.CONSUMED(target))
        q = q.replace("(" + v, "(" + Format.CONSUMED(target))
        q = q[1:]
        return q
    if step == "execute2":
        return s.calc_fullname()
    if step == "recursion":
        return s.calc_fullname()


def pretty_tape(tape):
    if not hasattr(tape, "step") or tape.step is None:
        if tape.name:
            return Format.NAME(tape.name)
        return tape.calc_fullname()

    if tape.step == "expanded":
        return tape.calc_fullname()


def pretty(s):
    if type(s) == Abstraction:
        return pretty_lambda(s)
    if type(s) == Tape:
        return pretty_tape(s)

    print("not valid pretty type", s, type(s))
    exit()


class Tape():

    def __init__(self, *items, name=None):
        global KNOWN_NAMES
        self.name = name
        if name is not None and name not in KNOWN_NAMES:
            KNOWN_NAMES[name] = self

        items = [Tape(*item) if type(item) == tuple else item for item in items]

        self.items = items
        self.fullname = self.calc_fullname()

    def __or__(self, other):
        return Tape(*self.items, other)

    def calc_fullname(self):
        if len(self) == 0:
            return "Empty"

        buf = []
        for item in self.items:
            text = str(item)
            if type(item) == Tape:
                text = "(%s)" % text
            buf.append(text)

        return " ".join(buf)

    def __repr__(self):
        global PRETTY
        if PRETTY:
            return pretty(self)

        if self.name:
            return self.name

        return self.fullname

    @classmethod
    def clone(cls, tape):
        items = [item for item in tape.items]
        new_tape = Tape(*items, name=tape.name)

        if hasattr(tape, "step"):
            new_tape.step = tape.step

        if hasattr(tape, "next_step"):
            new_tape.next_step = tape.next_step

        return new_tape

    def step_exec(self):
        self = Tape.clone(self)

        if not hasattr(self, "step"):
            self.step = None

        if not hasattr(self, "next_step"):
            self.next_step = None

        self.step = self.next_step

        if self.step is None:
            if self.name is not None:
                self.next_step = "expanded"
                return self
            else:
                self.step = "expanded"
                self.next_step = self.step

        if self.step == "expanded":
            self.next_step = self.step

        items = []
        done_something = False
        has_callable = False

        # print(print_tree(self))

        for item in self.items:
            has_callable = has_callable | callable(item)
            if type(item) == Tape and not done_something:
                try:
                    new_item = item()
                    # print("got return", new_item, type(new_item))
                    done_something = True
                    item = new_item
                except EOFError:
                    print("got here")
                    print(self, len(self))
                    print(print_tree(self))
                    exit()
                    item = item.pop()
                    item.step = None
                    item.next_step = None
                    done_something = False
                    pass
            items.append(item)
            self.items = items
        if done_something:
            # print("Tape done something", self.items)
            return self
        if not has_callable:
            return tuple(self.items)

        f = self.pop()
        # print("Tape pop", f)

        if not callable(f):
            return tuple([f, *self.items])

        try:
            f = f(self)
        except EOFError:
            f = Abstraction.clone(f)
            f.step = None
            f.next_step = None
            return f

        if type(f) == tuple and len(f) == 1:
            f = f[0]

        if type(f) == tuple:
            f = Tape(*f)
            return f

        if not callable(f):
            return f

        t = f >> self
        t.name = self.name
        t.next_step = self.next_step
        t.step = self.step
        return t

    def __call__(self):
        from inspect import stack, getmodule
        global PRETTY

        frm = stack()[1]
        mod = getmodule(frm[0]).__name__

        if len(self.items) == 0:
            return None

        # print("Tape(%s)" % (self.items))
        if mod != "__main__":
            res = self.step_exec()
            # print("Tape received res", res, type(res))
            return res

        f = self
        previous_print = None
        count_loop = 0

        while True:
            try:
                f = f()
                if type(f) == Abstraction:
                    return f
                if is_final(f):
                    return f


                PRETTY = True
                s = str(f)
                print(s)
                if s == previous_print:
                    count_loop += 1
                    if count_loop >= 10:
                        print("loop")
                        exit()
                else:
                    count_loop = 0
                previous_print = s
                PRETTY = False

            except EOFError:
                break

        print()
        return f

    def pop(self):
        item = self.items.pop(0)
        self.fullname = self.calc_fullname()
        return item

    def __len__(self):
        return len(self.items)


class Abstraction():

    def __init__(self, f, args=None, body=None, name=None):
        from inspect import signature, stack
        global KNOWN_NAMES

        if name is None:
            frameinfo = stack()[1]
            code_context = frameinfo.code_context[0]
            self.name = code_context.split("Abstraction")[0].rstrip(" =")
        else:
            self.name = name

        if self.name is not None and self.name not in KNOWN_NAMES:
            KNOWN_NAMES[self.name] = self

        if args is None:
            args = list(signature(f).parameters)

        self.args = args
        if body is None:
            body_str = get_source(f).split(": ")[1]
            values = {value: value for index, value in enumerate(self.args)}
            values = values | KNOWN_NAMES
            body = eval(body_str, values)
            del body_str
            del values

        self.body = body
        self.fullname = self.calc_fullname()

        self.make_function()

    def calc_fullname(self):

        def rec(items, args=0):
            global PRETTY
            res = []
            if type(items) == str:
                return items
            for item in items:
                old_pretty = PRETTY
                PRETTY = False
                s2 = str(item)
                PRETTY = old_pretty
                if item == items[0] and args > 0 and s2[0] == "λ":
                    item = "(" + str(item) + ")"

                s = str(item)
                if type(item) == tuple:
                    s = "(%s)" % rec(item)
                if type(item) == Tape:
                    s = "(%s)" % s
                res.append(s)
            return " ".join(res)

        s_body = rec(self.body, len(self.args))

        return "".join(["λ%s." % arg for arg in self.args]) + s_body


    @classmethod
    def partial(cls, args, body):
        return Abstraction(None, args=args, body=body, name=False)

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

        return self.fullname

    def __rshift__(self, other):
        return Tape(self, *other.items)

    def __or__(self, other):
        temp_name = "%s | %s" % (str(self), str(other))

        from inspect import stack
        frameinfo = stack()[1]
        code_context = frameinfo.code_context[0].rstrip()
        var_name = code_context.split(" = ")[0].rstrip()

        if var_name + " = " + temp_name == code_context:
            name = var_name
        else:
            name = None

        if type(other) == tuple:
            return Tape(Abstraction.clone(self), Tape(*other), name=name)

        return Tape(Abstraction.clone(self), other, name=name)

    def __call__(self, tape):
        self = Abstraction.clone(self)

        if not hasattr(self, "step"):
            self.step = None

        if hasattr(self, "next_step"):
            self.step = self.next_step

        # print("Abs(%s)[%s]{%s}" % (self.step, self.args, self.body))

        if self.step == "recursion" and len(tape) > 0:
            self.step = None
            # exit()

        if self.step is None:
            if self.name:
                # print("%s -> %s" % (self.step, self.next_step))
                self.next_step = "expand"
            else:
                if len(tape) == 0:
                    self.next_step = "recursion"
                else:
                    self.next_step = "prepare"
            return self

        if self.step == "expand":
            self.name = None
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
            # print("  consuming", self.args[0], self.body, self.target)
            res_body = self.f(self.target)
            # print("  execute response", res_body, type(res_body))
            if type(res_body) != tuple:
                res_body = (res_body,)
            self.args = self.args[1:]
            # print("args left", self.args)

            if len(self.args) == 0:
                return res_body

            self.next_step = None
            self.body = res_body

            return self

            if len(self.args) > 0:
                # print("  returning new Abstraction")
                return Abstraction.partial(args=self.args, body=res_body)(tape)(tape)

            if len(res_body) == 1:
                # print("  returning single element")
                res_body = res_body[0]

            return res_body

        if self.step == "recursion":

            def exec_rec(body):
                t = Tape(*body)
                if is_final(t):
                    raise EOFError

                res = t()
                # print("received res", res, type(res))
                if type(res) != Tape:
                    return res

                return tuple(res.items)

            res = exec_rec(self.body)

            if type(res) == Abstraction:
                raise EOFError

            if type(res) != tuple and len(self.args) == 0:
                return res

            if type(res) != tuple:
                res = (res,)

            self.body = res

            self.fullname = self.calc_fullname()
            return self

    @classmethod
    def clone(cls, self):
        from copy import deepcopy
        f = self.f
        args = self.args.copy()
        body = deepcopy(self.body)

        clone = Abstraction(f, args, body)
        clone.name = self.name

        if hasattr(self, "step"):
            clone.step = self.step
        if hasattr(self, "next_step"):
            clone.next_step = self.next_step
        if hasattr(self, "target"):
            clone.target = self.target

        return clone
