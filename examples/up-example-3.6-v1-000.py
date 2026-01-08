from pprint import pprint
import sympy as sp

from combine_equations.kinematics_states import (
    make_states_model,
    kinematics_fundamental,
)

from combine_equations.solve_system import solve_system_2
from combine_equations.solve_system import solve_system_multiple_solutions
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

def solve_and_display(equations, values, want):
    tmp = solve_system_2(equations, values, want)
    display_equation_(tmp, values, want=want)
    display_equation_(tmp.subs(values), values, want=want)

def solve_and_display_(equations, values, want):
    
    tmp = solve_system_multiple_solutions(equations, values, want)
    
    for index, sol in enumerate(tmp):
        if len(tmp) > 1:
            print(f"Solution {index+1}:")
        display_equation_(sol, values, want=want)
        display_equation_(sol.subs(values), values, want=want)
# ----------------------------------------------------------------------
# A motorcycle stunt rider
# rides off the edge of a cliff.
# 
# Just at the edge
# his velocity is horizontal,
# with magnitude 9.0 m/s.
# 
# Find
# the motorcycle’s position,
# distance from the edge of the cliff,
# and velocity
# 0.50 s after it leaves the edge of the cliff.
# 
# Ignore air resistance.
# ----------------------------------------------------------------------

m = make_states_model('m', 2)

m0, m1 = m.states

m01 = m.edges[0]

eqs = kinematics_fundamental(m, axes=['x', 'y'])

display_equations_(eqs)

# ----------------------------------------------------------------------

# projectile motion

g = sp.symbols('g')

eqs += eq_flat(
    m0.pos.x, 0,
    m0.pos.y, 0,
    
    m01.a.x,  0,
    m01.a.y, -g,

    m0.t, 0,


)

eqs = eliminate_zero_eqs(eqs)

display_equations_(eqs)

values = {}

# Just at the edge
# his velocity is horizontal,
# with magnitude 9.0 m/s.

values[m0.vel.x] = 9.0  # m/s
values[m0.vel.y] = 0.0  # m/s

values[m1.vel.x] = 9.0  # m/s

values[g]        = 9.8  # m/s^2

# Find
# the motorcycle’s position,
# distance from the edge of the cliff,
# and velocity
# 0.50 s after it leaves the edge of the cliff.

values[m1.t] = 0.50  # s

display_equations_(eqs, values)

# ----------------------------------------------------------------------
# Find the motorcycle’s position
# ----------------------------------------------------------------------

want = m1.pos.x

display_equations_(eqs, values, want=m1.pos.x)

# tmp = eqs
# tmp, _ = eliminate_variable_subst(tmp, m01.dt)
# tmp, _ = eliminate_variable_subst(tmp, m01.a.y)
# tmp, _ = eliminate_variable_subst(tmp, m01.v_av.x)
# tmp, _ = eliminate_variable_subst(tmp, m01.v_av.y)
# tmp, _ = eliminate_variable_subst(tmp, m1.vel.y)

# display_equations_(tmp, values, want=m1.pos.x)

# solve_and_display_(tmp, values, want=m1.pos.x)

# equations = tmp
# want = m1.pos.x

# var = m1.pos.x
# max_passes = 10

# eq = eqs[0]
# eq = eqs[1]

# tmp, _ = eliminate_variable_subst(tmp, m1.pos.y)

# display_equations_(tmp, values, want=want)

# values
# want
# solve_and_display_(tmp, values, want=want)



solve_and_display_(eqs, values, want=m1.pos.x)

display_equations_(eqs, values, want=want)

# display_equations_(equations, values, want=want)