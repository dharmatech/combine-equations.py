
import sympy as sp
from combine_equations.display_equations import display_equation_
from combine_equations.misc import multiply_both_sides, add_both_sides

# ----------------------------------------------------------------------
def solve_subs(eq_a, eq_b, var):

    result = sp.solve(eq_b, var)

    if len(result) == 1:
        return eq_a.subs(var, result[0])

    raise ValueError("Multiple solutions found; cannot substitute uniquely.")

def symbols_in_common(eq_a, eq_b):
    return eq_a.free_symbols.intersection(eq_b.free_symbols)

def isolate_variable(eq, var):
    sol = sp.solve(eq, var)
    if len(sol) == 1:
        # return sol[0]
        return sp.Eq(var, sol[0])
    raise ValueError("Multiple solutions found; cannot isolate uniquely.")
# ----------------------------------------------------------------------
x_1 = sp.symbols('x_1')
x_2 = sp.symbols('x_2')
v_1x = sp.symbols('v_1x')
v_2x = sp.symbols('v_2x')
v_av_x = sp.symbols('v_av_x')
t_1 = sp.symbols('t_1')
t_2 = sp.symbols('t_2')
dt = sp.symbols('dt')
a_x = sp.symbols('a_x')
# ----------------------------------------------------------------------
# Core equations from the book.
# They are not derived from anything else.

# eq 2.2
# v_av_x = (x_2 - x_1) / dt

# eq 2.7
# a_x = (v_2x - v_1x) / dt

# eq 2.10
# v_av_x = (v_1x + v_2x) / 2
# ----------------------------------------------------------------------
eq_2_2 = sp.Eq(v_av_x, (x_2 - x_1) / dt)

eq_2_7 = sp.Eq(a_x, (v_2x - v_1x) / dt)

eq_2_10 = sp.Eq(v_av_x, (v_1x + v_2x) / 2)

tmp = solve_subs(eq_2_2, eq_2_7, dt)
display_equation_(tmp)
# v_av_x = a_x*(-x_1 + x_2)/(-v_1x + v_2x)

tmp = solve_subs(eq_2_2, eq_2_10, v_av_x)
tmp = multiply_both_sides(tmp, dt)
tmp = sp.simplify(tmp)
tmp = multiply_both_sides(tmp, -1)
display_equation_(tmp)
# -x_1 + x_2 = dt*(v_1x + v_2x)/2
# This is eq 2.14 from the book.

tmp = isolate_variable(eq_2_7, v_2x)
display_equation_(tmp)
# v_2x = a_x*dt + v_1x
# This is equation 2.8 from the book.

tmp = solve_subs(eq_2_2, eq_2_7, dt)
tmp = solve_subs(tmp, eq_2_10, v_av_x)
tmp = multiply_both_sides(tmp, (-v_1x + v_2x))
tmp = multiply_both_sides(tmp, 2)
tmp = sp.simplify(tmp)
tmp = add_both_sides(tmp, v_1x**2)
display_equation_(tmp)
# 2*a_x*(-x_1 + x_2) + v_1x**2 = v_2x**2
# This is eq 2.13 from the book.

tmp = solve_subs(eq_2_2, eq_2_10, v_av_x)
tmp = solve_subs(tmp, eq_2_7, v_2x)
tmp = isolate_variable(tmp, x_2)
display_equation_(tmp)
# x_2 = a_x*dt**2/2 + dt*v_1x + x_1
# This is eq 2.12 from the book.
