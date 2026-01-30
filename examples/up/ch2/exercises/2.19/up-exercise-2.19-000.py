# An antelope 
# moving with constant acceleration 
# covers the distance between two points 70.0 m apart 
# in 6.00 s.
# 
# Its speed as it passes the second point is 15.0 m/s.
# 
# What are 
# (a) its speed at the first point and
# (b) its acceleration?
# ----------------------------------------------------------------------
from pprint import pprint
import sympy as sp

from sympy.physics.units import newton, meter, second, meters
from sympy.physics.units import N, m, s, km, h

from combine_equations.kinematics_states import *
from combine_equations.solve_system import *
from combine_equations.display_equations import display_equations_
from combine_equations.solve_and_display import solve_and_display_
from combine_equations.misc import eq_flat
from combine_equations.newtons_laws import *
# ----------------------------------------------------------------------
o = make_states_model("o", 2)  # antelope

o0, o1 = o.states

o01 = o.edges[0]

eqs = kinematics_fundamental(o, axes=['x'])
# ----------------------------------------------------------------------
values = {}

values[o0.pos.x] =  0    * m
values[o1.pos.x] = 70.0  * m
values[o01.dt]   =  6.00 * s
values[o1.vel.x] = 15.0  * m/s
# ----------------------------------------------------------------------
display_equations_(eqs, values, want=o0.vel.x)
solve_and_display_(eqs, values, want=o0.vel.x)
# o_0_v_x = (-dt_o_0_1*o_1_v_x - 2*o_0_x + 2*o_1_x)/dt_o_0_1
# o_0_v_x = 8.33333333333333*meter/second
# ----------------------------------------------------------------------
display_equations_(eqs, values, want=o01.a.x)
solve_and_display_(eqs, values, want=o01.a.x)
# a_x_o_0_1 = (2*dt_o_0_1*o_1_v_x + 2*o_0_x - 2*o_1_x)/dt_o_0_1**2
# a_x_o_0_1 = 1.11111111111111*meter/second**2

