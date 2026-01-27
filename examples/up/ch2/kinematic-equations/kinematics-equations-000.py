
import sympy as sp

# ----------------------------------------------------------------------

def solve_subs(eq_a, eq_b, var):

    result = sp.solve(eq_b, var)

    if len(result) == 1:
        return eq_a.subs(var, result[0])

    raise ValueError("Multiple solutions found; cannot substitute uniquely.")

def symbols_in_common(eq_a, eq_b):
    return eq_a.free_symbols.intersection(eq_b.free_symbols)

# ----------------------------------------------------------------------

x_1 = sp.symbols('x_1')
x_2 = sp.symbols('x_2')
v_1x = sp.symbols('v_1x')
v_2x = sp.symbols('v_2x')
v_av_x = sp.symbols('v_av_x')
t_1 = sp.symbols('t_1')
t_2 = sp.symbols('t_2')
a_x = sp.symbols('a_x')
# ----------------------------------------------------------------------

# eq 2.2
# v_av_x = (x_2 - x_1) / (t_2 - t_1)

# eq 2.7
# a_x = (v_2x - v_1x) / (t_2 - t_1)

# eq 2.10
# v_av_x = (v_1x + v_2x) / 2

# tmp_1   eq_2_2 and eq_2_7 eliminate t_2 - t_1
# a_x = v_av_x*(-v_1x + v_2x)/(-x_1 + x_2)

# tmp_1 and eq_2_10 in common: v_av_x, v_1x, v_2x



eq_2_2 = sp.Eq(v_av_x, (x_2 - x_1) / (t_2 - t_1))

eq_2_7 = sp.Eq(a_x, (v_2x - v_1x) / (t_2 - t_1))

eq_2_10 = sp.Eq(v_av_x, (v_1x + v_2x) / 2)


# tmp_1 = eq_2_7.subs(t_2 - t_1, sp.solve(eq_2_2, t_2 - t_1)[0])
# display_equation_(tmp_1)
# a_x = v_av_x*(-v_1x + v_2x)/(-x_1 + x_2)


eq_2_7.subs(t_2, sp.solve(eq_2_2, t_2)[0])


# solve_subs


solve_subs(eq_2_7, eq_2_2, t_2)
solve_subs(eq_2_7, eq_2_2, t_1)
solve_subs(eq_2_2, eq_2_7, t_2 - t_1)

# eq_2_7.free_symbols.intersection(eq_2_2.free_symbols)


symbols_in_common(eq_2_2, eq_2_7)
symbols_in_common(eq_2_2, eq_2_10)
symbols_in_common(eq_2_7, eq_2_10)






# tmp_1
# eq 2.2 and 2.7 eliminate t_2 - t_1

# tmp_1 and eq 2._10 eliminate (v_1x + v_2x)

# eq_2_2 = sp.Eq((v_1x + v_2x) / 2, (x_2 - x_1) / (t_2 - t_1))

# eq_2_7 = sp.Eq(a_x, (v_2x - v_1x) / (t_2 - t_1))

# eq_2_10 = sp.Eq((v_1x + v_2x) / 2, v_1x + a_x * (t_2 - t_1) / 2)

display_equation_(eq_2_10)

sp.simplify(eq_2_10)

# solve eq 2.7 for v_2x. subsitute into eq 2.10
# notation:
# eq 2.10 /. eq 2.7 v_2x
#
# eq 2.10 substitue eq 2.7 solved for v_2x
#
# gives us eq 2.11

# eq 2.2 and eq 2.11. eliminate v_av_x

# eq 2.2   and   eq 2.10   eliminate v_av_x
# eq 2.7   and   eq 2.10   eliminate v_2x


# eq 2.2
# eq 2.7
# in common: t_2, t_1, t_2 - t_1

from combine_equations.display_equations import *

display_equation_(eq_2_2)

sp.solve([eq_2_2, eq_2_7], t_2)

sp.solve(eq_2_2, t_2 - t_1)

tmp_1 = eq_2_7.subs(t_2 - t_1, sp.solve(eq_2_2, t_2 - t_1)[0])

display_equation_(tmp_1)
# a_x = (-v_1x + v_2x)*(v_1x + v_2x)/(2*(-x_1 + x_2))

from combine_equations.eliminate_variable_subst import *

# eliminate_variable_subst(eq_2_2, eq_2_7, t_2 - t_1)


# tmp_1 and eq 2._10 eliminate (v_1x + v_2x)

sp.solve(eq_2_10, (v_1x + v_2x))