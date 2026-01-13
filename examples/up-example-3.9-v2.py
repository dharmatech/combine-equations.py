
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
    magnitude_and_angle_equations,
)

from combine_equations.kinematics_states import State
from combine_equations.solve_system import *
from combine_equations.display_equations import display_equations_
from combine_equations.eliminate_variable_subst import eliminate_zero_eqs
from combine_equations.solve_and_display import solve_and_display_
from combine_equations.misc import eq_flat
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
# b_1_t = dt_b_0_1
# v_av_x_b_0_1 = b_1_x/dt_b_0_1
# v_av_y_b_0_1 = -b_0_y/dt_b_0_1
# (-b_0_v_x + b_1_v_x)/dt_b_0_1 = 0
# a_y_b_0_1 = (-b_0_v_y + b_1_v_y)/dt_b_0_1
# b_0_v_x = -b_1_v_x + 2*v_av_x_b_0_1
# b_0_v_y = -b_1_v_y + 2*v_av_y_b_0_1
# a_y_b_0_1 = -g
# b_0_v_x = b_1_v_x
# b_0_v_x = b_0_v_mag*cos(b_0_v_angle)
# b_0_v_y = b_0_v_mag*sin(b_0_v_angle)
# b_0_v_mag = sqrt(b_0_v_x**2 + b_0_v_y**2)
# b_0_v_angle = atan2(b_0_v_y, b_0_v_x)

solve_and_display_(eqs, values, want=b1.pos.x, version=2)

# Solution 1:
# b_1_x = b_0_v_mag*(b_0_v_mag*sin(b_0_v_angle) - sqrt(b_0_v_mag**2*sin(b_0_v_angle)**2 + 2*b_0_y*g))*cos(b_0_v_angle)/g
# b_1_x = -15.7161745661753

# Solution 2:
# b_1_x = b_0_v_mag*(b_0_v_mag*sin(b_0_v_angle) + sqrt(b_0_v_mag**2*sin(b_0_v_angle)**2 + 2*b_0_y*g))*cos(b_0_v_angle)/g
# b_1_x = 9.16380341748480

