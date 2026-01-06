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

# You throw a ball vertically upward
# from the roof of a tall building.
#
# The ball leaves your hand
# at a point even with the roof railing
# with an upward speed of 15.0 m/s;
# the ball is then in free fall.
# (We ignore air resistance.)
# On its way back down, it just misses the railing.
#
# Find
#
# (a) the ball’s position and velocity
# 1.00 s and 4.00 s after leaving your hand;
#
# (b) the ball’s velocity when it is 5.00 m above the railing;
#
# (c) the maximum height reached;
#
# (d) the ball’s acceleration when it is at its maximum height.

b = make_states_model("b", 2)  # ball

pprint(b)

b0, b1 = b.states

b01 = b.edges[0]

eqs = []
eqs += kinematics_fundamental(b, axes=['y'])

eqs += eq_flat(
    b0.t,     0,
    b0.pos.y, 0
)

display_equations_(eqs)

eqs = eliminate_zero_eqs(eqs)

display_equations_(eqs)

values = {}

# You throw a ball vertically upward
# from the roof of a tall building.
#
# The ball leaves your hand
# at a point even with the roof railing
# with an upward speed of 15.0 m/s;

values[b0.vel.y] = 15.0  # m/s

# the ball is then in free fall.

values[b01.a.y] = -9.8  # m/s^2

# (We ignore air resistance.)
# On its way back down, it just misses the railing.
#
# Find
#
# (a) the ball’s position and velocity
# 1.00 s and 4.00 s after leaving your hand;

values[b1.t] = 1.0  # s

display_equations_(eqs, values, want=b1.pos.y)

solve_and_display(eqs, values, want=b1.pos.y)
solve_and_display_(eqs, values, want=b1.pos.y)
# b_1_y = b_1_t*(a_y_b_0_1*b_1_t + 2*b_0_v_y)/2
# b_1_y = 10.1000000000000

solve_and_display(eqs, values, want=b1.vel.y)
# b_1_v_y = a_y_b_0_1*b_1_t + b_0_v_y
# b_1_v_y = 5.20000000000000

values[b1.t] = 4.0  # s

solve_and_display(eqs, values, want=b1.pos.y)
# b_1_y = b_1_t*(a_y_b_0_1*b_1_t + 2*b_0_v_y)/2
# b_1_y = -18.4000000000000

solve_and_display(eqs, values, want=b1.vel.y)
# b_1_v_y = a_y_b_0_1*b_1_t + b_0_v_y
# b_1_v_y = -24.2000000000000

# t=0 y=  0   v= 15
# t=1 y= 10.1 v=  5.2
# t=4 y=-18.4 v=-24.2

# ----------------------------------------------------------------------
# (b) the ball’s velocity when it is 5.00 m above the railing;

values = {}
values[b0.vel.y] = 15.0  # m/s
values[b01.a.y]  = -9.8  # m/s^2
values[b1.pos.y] =  5.0  # m

display_equations_(eqs, values, want=b1.vel.y)

# equations = eqs
# want = b1.vel.y

solve_and_display(eqs, values, want=b1.vel.y)
# b_1_v_y = -sqrt(2*a_y_b_0_1*b_1_y + b_0_v_y**2)
# b_1_v_y = -11.2694276695846

# We should get two solutions here.

# tmp = solve_system_multiple_solutions(eqs, values, want=b1.vel.y)

# for index, sol in enumerate(tmp):
#     print(f"Solution {index+1}:")
#     display_equation_(sol, values, want=b1.vel.y)
#     display_equation_(sol.subs(values), values, want=b1.vel.y)

solve_and_display_(eqs, values, want=b1.vel.y)