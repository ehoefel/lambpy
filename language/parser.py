
import ply.lex as lex
import ply.yacc as yacc
from language.expression import Grouping, Variable, Abstraction
from language.expression import Application, Rule

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
    pass


def p_abstraction(p):
    'expression : LAMBDA variable-list DOT expression'
    p[0] = Abstraction(p[2][0], p[4])


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
    pass


lexer = lex.lex(optimize=1, debug=False)
parser = yacc.yacc(optimize=1, debug=False)


def parse(exp_str, rule_list=None):
    exp = parser.parse(exp_str, debug=False)
    if exp is None:
        return None
    if rule_list is not None:
        rule_list.apply(exp)
    if type(exp) == Variable:
        return None

    return exp
