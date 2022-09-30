from sympy import symbols, Eq, solve

x, y = symbols('x y')
eq1 = Eq(x + y - 8.784)
eq2 = Eq(x/1.2 - y/7.2 - 0.3)
sol = solve((eq1, eq2), (x, y))

print(sol[x])
