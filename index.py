from lambpy import Abstraction


TRUE = Abstraction(lambda x, y: x)
FALSE = Abstraction(lambda x, y: y)
AND = Abstraction(lambda p, q: (p, q, p))
OR = Abstraction(lambda p, q: (p, p, q))
NOT = Abstraction(lambda p: (p, FALSE, TRUE))
ZERO = Abstraction(lambda f, x: x)
SUCC = Abstraction(lambda n, f, x: (f, (n, f, x)))
ONE = SUCC | ZERO
PLUS = Abstraction(lambda m, n: (m, SUCC, n))
MULT = Abstraction(lambda m, n: (m, (PLUS, n), ZERO))

# print((TRUE | FALSE | TRUE)())
# print((FALSE | TRUE | FALSE)())
# print((AND | TRUE | FALSE)())
# print((NOT | TRUE)())
# print((NOT | FALSE)())
# print((SUCC | ZERO)())
# print((SUCC | (SUCC | ZERO))())
# print((SUCC | (SUCC | (SUCC | ZERO)))())
# print((PLUS | ZERO | ZERO)())
# print((PLUS | ZERO | (SUCC | ZERO))())
# print((MULT | ZERO | ZERO)())
# print((MULT | ZERO | ONE)())
# print((MULT | ONE | ZERO)())
print((MULT | ONE | ONE)())

