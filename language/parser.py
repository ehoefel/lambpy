
import ply.lex as lex
import ply.yacc as yacc
from expression import Grouping, Variable, Abstraction, Application, Rule
from expression import bind

tokens = (
    'VAR',
    'LAMBDA',
    'LPAREN',
    'RPAREN',
    'DOT',
)

t_VAR = r'[a-zA-Z0-9]+'
t_LAMBDA = r'λ'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_DOT = r'\.'
t_ignore = ' \r\n'


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    exit()


def p_abstraction(p):
    'expression : LAMBDA variable-list DOT expression'

    if len(p[2]) > 1:
        print("abstraction with multiple variables")
        print(p[2])
        exit()

    p[0] = Abstraction(p[2][0], p[4])

#     ab = None
#     for el in reversed(p[2]):
#         if ab is None:
#             ab = Abstraction(el, p[4])
#         else:
#             ab = Abstraction(el, el)
#     p[0] = ab


def p_variable_list(p):
    'variable-list : variable'
    p[0] = [p[1]]


def p_variable_list2(p):
    'variable-list : variable variable-list'
    p[0] = [p[1]] + p[2]


def p_expression(p):
    '''expression : application-term'''
    p[0] = p[1]


def p_application_term(p):
    '''application-term : application-term item'''
    p[0] = Application(p[1], p[2])


def p_item(p):
    '''application-term : item'''
    p[0] = p[1]


def p_variable(p):
    '''item : variable'''
    p[0] = p[1]


def p_grouping(p):
    '''item : LPAREN expression RPAREN'''
    p[0] = Grouping(p[2])


def p_variable2(p):
    'variable : VAR'
    p[0] = Variable(p[1])


def p_error(p):
    print("Syntax error in input!")
    print(p)


lexer = lex.lex(optimize=1, debug=False)
parser = yacc.yacc(optimize=1)

rules = []


def parse(exp_str):
    exp = parser.parse(exp_str)
    for rule in rules:
        bind(exp, rule)
        # exp.bind(rule)

    return exp


def rule(name, exp_str):
    rule = Rule(name, parse(exp_str))
    rules.append(rule)
    return rule


if __name__ == "__main__":

    rule("SUCC", "λn.λf.λx.f(n f x)")
    rule("0", "λf.λx.x")
    rule("PLUS", "λm.λn.m SUCC n")
    exp = parse("PLUS (SUCC 0) (SUCC 0)")
    import code
    code.interact(local=locals())
