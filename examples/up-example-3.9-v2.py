
# You throw a ball from your window 8.0 m above the ground.
#
# When the ball leaves your hand, 
# it is moving at 10.0 m/s 
# at an angle of 20.0° below the horizontal.
# 
# How far horizontally from your window will the
# ball hit the ground? Ignore air resistance.
# ----------------------------------------------------------------------

from pprint import pprint
import sympy as sp

from combine_equations.kinematics_states import (
    make_states_model,
    kinematics_fundamental,
)

from combine_equations.solve_system import *
# from combine_equations.solve_system import solve_system_multiple_solutions, solve_system_multiple_solutions_000
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

def solve_and_display_(equations, values, want, version=1):
    
    if version == 1:
        tmp = solve_system_multiple_solutions(equations, values, want)
    elif version == 0:
        tmp = solve_system_multiple_solutions_000(equations, values, want)
    elif version == 2:
        tmp = solve_with_elimination_attempts(equations, values, want)
    else:
        raise ValueError(f"Unsupported version: {version}")
    
    for index, sol in enumerate(tmp):
        if len(tmp) > 1:
            print(f"Solution {index+1}:")
        display_equation_(sol, values, want=want)
        # display_equation_(sol.subs(values), values, want=want)
        display_equation_(sp.N(sol.subs(values)), values, want=want)

from combine_equations.kinematics_states import State

def magnitude_and_angle_equations(obj: State) -> list:
    eqs = eq_flat(
        obj.vel.x,    obj.vel.mag*sp.cos(obj.vel.angle),
        obj.vel.y,    obj.vel.mag*sp.sin(obj.vel.angle),

        obj.vel.mag,   sp.sqrt(obj.vel.x**2 + obj.vel.y**2),
        obj.vel.angle, sp.atan2(obj.vel.y, obj.vel.x)
    )

    return eqs        
# ----------------------------------------------------------------------

b = make_states_model('b', 2)

b0, b1 = b.states

b01 = b.edges[0]

eqs = kinematics_fundamental(b, axes=['x', 'y'])

display_equations_(eqs)

# ----------------------------------------------------------------------
# projectile motion

g = sp.symbols('g')

# You throw a ball from your window 8.0 m above the ground.

eqs += eq_flat(
    b0.pos.x, 0,
    # b0.pos.y, 8.0,

    b01.a.x, 0,
    b01.a.y, -g,

    b0.t, 0,

    b0.vel.x, b1.vel.x,

    b1.pos.y, 0 # hits ground
)

eqs = eliminate_zero_eqs(eqs)

display_equations_(eqs)
# ----------------------------------------------------------------------

values = {}

values[g] = 9.81 # m/s^2

values[b0.pos.y] = 8.0 # m

# When the ball leaves your hand, 
# it is moving at 10.0 m/s 
# at an angle of 20.0° below the horizontal.

eqs += magnitude_and_angle_equations(b0)

values[b0.vel.mag] = 10.0 # m/s
values[b0.vel.angle] = sp.N(sp.rad(-20.0)) # degrees to radians
# ----------------------------------------------------------------------
# How far horizontally from your window will the
# ball hit the ground? Ignore air resistance.
# ----------------------------------------------------------------------
display_equations_(eqs, values, want=b1.pos.x)

solve_and_display_(eqs, values, want=b1.pos.x, version=2)

# Solution 1:
# b_1_x = b_0_v_mag*(b_0_v_mag*sin(b_0_v_angle) - sqrt(b_0_v_mag**2*sin(b_0_v_angle)**2 + 2*b_0_y*g))*cos(b_0_v_angle)/g
# b_1_x = -15.7161745661753

# Solution 2:
# b_1_x = b_0_v_mag*(b_0_v_mag*sin(b_0_v_angle) + sqrt(b_0_v_mag**2*sin(b_0_v_angle)**2 + 2*b_0_y*g))*cos(b_0_v_angle)/g
# b_1_x = 9.16380341748480

