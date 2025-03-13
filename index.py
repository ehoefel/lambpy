from lambdu import Lambda


TRUE = Lambda(lambda x, y: x)
FALSE = Lambda(lambda x, y: y)
AND = Lambda(lambda p, q: (p, q, p))
OR = Lambda(lambda p, q: (p, p, q))
ZERO = Lambda(lambda f, x: x)
SUCC = Lambda(lambda n, f, x: (f, (n, f, x)))
ONE = SUCC | ZERO

# print((SUCC | ZERO)())
print((SUCC | ONE)())
# print((AND | TRUE | FALSE)())

