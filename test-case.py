
import sympy as sp

a = sp.symbols('a')

sp.simplify(sp.Eq(1, sp.atan2(a, 2/a)))

