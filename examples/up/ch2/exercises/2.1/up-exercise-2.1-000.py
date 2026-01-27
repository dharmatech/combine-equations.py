
# A car travels in the +x-direction on a straight and level road.
#
# For the first 4.00 s of its motion,
# the average velocity of the car is
# v_av_x = 6.25 m/s. 
# 
# How far does the car travel in 4.00 s?
# ----------------------------------------------------------------------
from pprint import pprint
import sympy as sp

from sympy.physics.units import newton, meter, second, meters
from sympy.physics.units import N, m, s

from combine_equations.kinematics_states import *
from combine_equations.solve_system import *
from combine_equations.display_equations import display_equations_
from combine_equations.solve_and_display import solve_and_display_
from combine_equations.misc import eq_flat
from combine_equations.newtons_laws import *
# ----------------------------------------------------------------------

c = make_states_model("c", 2)  # car

c0, c1 = c.states

c01 = c.edges[0]

eqs = kinematics_fundamental(c, axes=['x'])
# ----------------------------------------------------------------------
values = {}

values[c0.pos.x]   = 0 * m
values[c0.t]       = 0 * s
values[c1.t]       = 4.0  * s
values[c01.v_av.x] = 6.25 * m/s
# ----------------------------------------------------------------------
display_equations_(eqs, values, c1.pos.x)

solve_and_display_(eqs, values, want=c1.pos.x)
# c_1_x = -c_0_t*v_av_x_c_0_1 + c_0_x + c_1_t*v_av_x_c_0_1
# c_1_x = 25.0*meter