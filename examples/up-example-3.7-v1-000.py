
# A batter hits a baseball
# so that it leaves the bat
# at speed v0 = 37.0 m/s
# at an angle a0 = 53.1°.
# 
# (a) Find the position of the ball 
# and its velocity (magnitude and direction) 
# at t = 2.00 s.
# 
# (b) Find the time 
# when the ball reaches the highest point of its flight, 
# and its height h at this time.
# 
# (c) Find the horizontal range R
# that is, the horizontal distance
# from the starting point to where the ball hits the ground
# and the ball’s velocity just before it hits.
# ----------------------------------------------------------------------

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
        # display_equation_(sol.subs(values), values, want=want)
        display_equation_(sp.N(sol.subs(values)), values, want=want)
# ----------------------------------------------------------------------
b = make_states_model('b', 2)

b0, b1 = b.states

b01 = b.edges[0]

eqs = kinematics_fundamental(b, axes=['x', 'y'])

display_equations_(eqs)
# ----------------------------------------------------------------------
# projectile motion

g = sp.symbols('g')

eqs += eq_flat(
    b0.pos.x, 0,
    b0.pos.y, 0,

    b01.a.x, 0,
    b01.a.y, -g,

    b0.t, 0,

    b0.vel.x, b1.vel.x
)

eqs = eliminate_zero_eqs(eqs)

display_equations_(eqs)
# ----------------------------------------------------------------------
values = {}

values[g] = 9.81 # m/s^2

# A batter hits a baseball
# so that it leaves the bat
# at speed v0 = 37.0 m/s
# at an angle a0 = 53.1°.

# v0, a0 = sp.symbols('v0 a0')

b0_vel_mag = sp.symbols('b0_vel_mag')
b0_vel_angle = sp.symbols('b0_vel_angle')

eqs += eq_flat(
    b0.vel.x, b0_vel_mag * sp.cos(b0_vel_angle),
    b0.vel.y, b0_vel_mag * sp.sin(b0_vel_angle),
)

pprint(b0)

values[b0_vel_mag] = 37.0 # m/s
values[b0_vel_angle] = sp.rad(53.1) # degrees to radians
# ----------------------------------------------------------------------
# (a) Find the position of the ball 
# and its velocity (magnitude and direction) 
# at t = 2.00 s.

values_a = values.copy()

values_a[b1.t] = 2.00 # s

display_equations_(eqs, values_a, want=b1.pos.x)
solve_and_display_(eqs, values_a, want=b1.pos.x)
# b_1_x = b0_vel_mag*b_1_t*cos(b0_vel_angle)
# b_1_x = 44.4310966741154

display_equations_(eqs, values_a, want=b1.pos.y)
solve_and_display_(eqs, values_a, want=b1.pos.y)
# b_1_y = b_1_t*(2*b0_vel_mag*sin(b0_vel_angle) - b_1_t*g)/2
# b_1_y = 39.5566647280447

display_equations_(eqs, values_a, want=b1.vel.x)
solve_and_display_(eqs, values_a, want=b1.vel.x)
# b_1_v_x = b0_vel_mag*cos(b0_vel_angle)
# b_1_v_x = 22.2155483370577

display_equations_(eqs, values_a, want=b1.vel.y)
solve_and_display_(eqs, values_a, want=b1.vel.y)
# b_1_v_y = b0_vel_mag*sin(b0_vel_angle) - b_1_t*g
# b_1_v_y = 9.96833236402235

b1_vel_mag = sp.symbols('b1_vel_mag')
b1_vel_angle = sp.symbols('b1_vel_angle')

eqs += eq_flat(
    b1_vel_mag, sp.sqrt(b1.vel.x**2 + b1.vel.y**2),
    b1_vel_angle, sp.atan2(b1.vel.y, b1.vel.x)
)

display_equations_(eqs, values_a, want=b1_vel_mag)
solve_and_display_(eqs, values_a, want=b1_vel_mag)
# b1_vel_mag = sqrt(b0_vel_mag**2 - 2*b0_vel_mag*b_1_t*g*sin(b0_vel_angle) + b_1_t**2*g**2)
# b1_vel_mag = 24.3495018026193

display_equations_(eqs, values_a, want=b1_vel_angle)
solve_and_display_(eqs, values_a, want=b1_vel_angle)
# b1_vel_angle = atan2(b0_vel_mag*sin(b0_vel_angle) - b_1_t*g, b0_vel_mag*cos(b0_vel_angle))
# b1_vel_angle = 0.421780406158419





b1_vel_angle_deg = sp.symbols('b1_vel_angle_deg')

eqs += eq_flat(
    b1_vel_angle_deg, sp.deg(b1_vel_angle)
)



display_equations_(eqs, values_a, want=b1_vel_angle_deg)

# For some reason, we need to eliminate `b1_vel_angle` manually first.
# Research this to see if our solver can handle this automatically. 
tmp, _ = eliminate_variable_subst(eqs, b1_vel_angle)
display_equations_(tmp, values_a, want=b1_vel_angle_deg)
eqs = tmp



display_equations_(eqs, values_a, want=b1_vel_angle_deg)
solve_and_display_(eqs, values_a, want=b1_vel_angle_deg)
# b1_vel_angle_deg = 180*atan2(b0_vel_mag*sin(b0_vel_angle) - b_1_t*g, b0_vel_mag*cos(b0_vel_angle))/pi
# b1_vel_angle_deg = 24.1662371541911

