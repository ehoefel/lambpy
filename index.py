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

# print((SUCC | ZERO)())
# print((SUCC | ONE)())
print((MULT | ONE | ONE)())
# print((AND | TRUE | FALSE)())

