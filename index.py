from lambdu import Lambda


TRUE = Lambda(lambda x, y: x)
FALSE = Lambda(lambda x, y: y)
AND = Lambda(lambda p, q: (p, q, p))
OR = Lambda(lambda p, q: (p, p, q))
NOT = Lambda(lambda p: (p, FALSE, TRUE))
ZERO = Lambda(lambda f, x: x)
SUCC = Lambda(lambda n, f, x: (f, (n, f, x)))
ONE = SUCC | ZERO
PLUS = Lambda(lambda m, n: (m, SUCC, n))
MULT = Lambda(lambda m, n: (m, (PLUS, n), ZERO))

print((TRUE | FALSE | TRUE)())
print((FALSE | TRUE | FALSE)())
print((AND | TRUE | FALSE)())
print((NOT | TRUE)())
print((NOT | FALSE)())
print((SUCC | ZERO)())
print((SUCC | (SUCC | ZERO))())
print((SUCC | (SUCC | (SUCC | ZERO)))())
print((PLUS | ZERO | ZERO)())
print((PLUS | ZERO | (SUCC | ZERO))())
print((MULT | ZERO | ZERO)())
print((MULT | ZERO | ONE)())
print((MULT | ONE | ZERO)())
# print((MULT | ONE | ONE)())

