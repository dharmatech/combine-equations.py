
# Find the 
# maximum height   h and 
# horizontal range R 
# (see Fig. 3.23) 
# of a projectile launched with speed v0 
# at an initial angle a0 between 0 and 90°.
# 
# For a given v0, 
# what value of a0 gives maximum height?
# 
# What value gives maximum horizontal range?

# ----------------------------------------------------------------------
from pprint import pprint
import sympy as sp

from combine_equations.kinematics_states import (
    make_states_model,
    kinematics_fundamental,
)

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

def solve_and_display_(equations, values, want):
    
    tmp = solve_system_multiple_solutions(equations, values, want)
    
    for index, sol in enumerate(tmp):
        if len(tmp) > 1:
            print(f"Solution {index+1}:")
        display_equation_(sol, values, want=want)
        # display_equation_(sol.subs(values), values, want=want)
        display_equation_(sp.N(sol.subs(values)), values, want=want)
# ----------------------------------------------------------------------

p = make_states_model('p', 2) # projectile

p0, p1 = p.states

p01 = p.edges[0]

eqs = kinematics_fundamental(p, axes=['x', 'y'])

display_equations_(eqs)
# ----------------------------------------------------------------------
# projectile motion

g = sp.symbols('g')

eqs += eq_flat(
    p0.pos.x, 0,
    p0.pos.y, 0,

    p01.a.x, 0,
    p01.a.y, -g,

    p0.t, 0,

    p0.vel.x, p1.vel.x
)

eqs = eliminate_zero_eqs(eqs)

display_equations_(eqs)
# ----------------------------------------------------------------------
# of a projectile launched with speed v0 
# at an initial angle a0 between 0 and 90°.

eqs += eq_flat(
    # p0.vel.x, p0.vel_mag*sp.cos(p0.vel_angle),
    # p0.vel.y, p0.vel_mag*sp.sin(p0.vel_angle)

    p0.vel.x,    p0.vel.mag * sp.cos(p0.vel.angle),
    p0.vel.y,    p0.vel.mag * sp.sin(p0.vel.angle),

    p0.vel.mag,   sp.sqrt(p0.vel.x**2 + p0.vel.y**2),
    p0.vel.angle, sp.atan2(p0.vel.y, p0.vel.x)
)

display_equations_(eqs)

# ----------------------------------------------------------------------
# Find the maximum height h

eqs_a = eqs.copy()

eqs_a += eq_flat(
    p1.vel.y, 0
)

eqs_a = eliminate_zero_eqs(eqs_a)

display_equations_(eqs_a, want=p1.pos.y)

values = {}

values[g] = 9.81 # m/s^2
values[p0.vel.mag]   = sp.symbols('v0') # m/s
values[p0.vel.angle] = sp.symbols('a0') # radians

display_equations_(eqs_a, values, want=p1.pos.y)

tmp = eqs_a
tmp, _ = eliminate_variable_subst(tmp, p0.vel.x)

display_equations_(tmp, values, want=p1.pos.y)

tmp_1 = solve_system_multiple_solutions(tmp, values, want=p1.pos.y)

display_equations_(tmp_1, values, want=p1.pos.y)

# ----------------------------------------------------------------------
# Find the horizontal range R 

eqs_b = eqs.copy()

eqs_b += eq_flat(
    p1.pos.y, 0
)

eqs_b = eliminate_zero_eqs(eqs_b)

display_equations_(eqs_b, values, want=p1.pos.x)


tmp_2 = solve_system_multiple_solutions(tmp, values, want=p1.pos.x)
# solve_and_display_(tmp, values, want=p1.pos.x)

display_equations_(tmp_2, values, want=p1.pos.x)
# ----------------------------------------------------------------------