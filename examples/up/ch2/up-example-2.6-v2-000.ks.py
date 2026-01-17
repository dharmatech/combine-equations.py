
# A one-euro coin is dropped from the Leaning Tower of Pisa and falls
# freely from rest. What are its position and velocity after 1.0 s, 2.0 s, and
# 3.0 s? Ignore air resistance.

from pprint import pprint
import sympy as sp

from combine_equations.kinematics_states import (
    make_states_model,
    kinematics_fundamental,
)

from combine_equations.solve_system import solve_system_2
from combine_equations.display_equations import display_equation_
from combine_equations.display_equations import display_equations_
from combine_equations.eliminate_variable_subst import eliminate_variable_subst

def eq_flat(*items):
    if len(items) % 2:
        raise ValueError(f"eq_flat needs an even number of items; got {len(items)}")
    return [sp.Eq(items[i], items[i+1]) for i in range(0, len(items), 2)]

# All items in eqs where right rhs is zero.

def eliminate_zero_eqs(equations):
    eqs_zero = [eq for eq in equations if eq.rhs == 0]
    tmp = equations
    for eq in eqs_zero:
        var = eq.lhs
        tmp, _ = eliminate_variable_subst(tmp, var)
    return tmp

# ----------------------------------------------------------------------

# A one-euro coin is dropped from the Leaning Tower of Pisa and falls
# freely from rest.

c = make_states_model("c", 2, include_v_av=True)  # coin

c0, c1 = c.states

c01 = c.edges[0]

eqs = []
eqs += kinematics_fundamental(c, axes=('y',))

display_equations_(eqs)


# equations.append(sp.Eq(c_0.t, 0))
# equations.append(sp.Eq(c_0.v, 0))
# equations.append(sp.Eq(c_0.x, 0))

eqs += eq_flat(
    c0.t, 0,
    c0.vel.y, 0,
    c0.pos.y, 0
)

display_equations_(eqs)

eqs = eliminate_zero_eqs(eqs)

# ----------------------------------------------------------------------
# endregion
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
# region solve
# ----------------------------------------------------------------------

values = {}

values[c01.a.y] = -9.8  # m/s^2

# What are its position and velocity after 1.0 s, 2.0 s, and
# 3.0 s? Ignore air resistance.

display_equations_(eqs, want=c1.pos.y)

values[c1.t] = 1.0  # s
tmp_a = solve_system_2(eqs, values=values, want=c1.pos.y)
display_equation_(tmp_a, values, want=c1.pos.y) # c_1_y = a_y_c_0_1*c_1_t**2/2
display_equation_(tmp_a.subs(values), values, want=c1.pos.y) # c_1_y = -4.9

tmp_a = solve_system_2(eqs, values=values, want=c1.vel.y)
display_equation_(tmp_a, values, want=c1.vel.y) # c_1_v_y = a_y_c_0_1*c_1_t
display_equation_(tmp_a.subs(values), values, want=c1.vel.y) # c_1_v_y = -9.8


values[c1.t] = 2.0  # s
tmp_a = solve_system_2(eqs, values=values, want=c1.pos.y)
display_equation_(tmp_a, values, want=c1.pos.y) # c_1_y = a_y_c_0_1*c_1_t**2/2
display_equation_(tmp_a.subs(values), values, want=c1.pos.y) # c_1_y = -19.6

values[c1.t] = 3.0  # s
tmp_a = solve_system_2(eqs, values=values, want=c1.pos.y)
display_equation_(tmp_a, values, want=c1.pos.y) # c_1_y = a_y_c_0_1*c_1_t**2/2
display_equation_(tmp_a.subs(values), values, want=c1.pos.y) # c_1_y = -44.1


# ----------------------------------------------------------------------
# endregion 
# ----------------------------------------------------------------------