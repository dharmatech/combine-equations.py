
# Trip Home.
# 
# You normally drive on the freeway between San Diego and Los Angeles 
# at an average speed of 105 km/h (65 mi/h),
# and the trip takes 1 h and 50 min.
# 
# On a Friday afternoon, however, heavy traffic slows you down 
# and you drive the same distance 
# at an average speed of only 70 km/h (43 mi/h).
# 
# How much longer does the trip take?

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
ca = make_states_model("ca", 2)  # car trip normal
cb = make_states_model("cb", 2)  # car trip slow

ca0, ca1 = ca.states
cb0, cb1 = cb.states

ca01 = ca.edges[0]
cb01 = cb.edges[0]

eqs = []

eqs += kinematics_fundamental(ca, axes=['x'])
# ----------------------------------------------------------------------

display_equations_(eqs)

values = {}

values[ca0.t] = 0 * h
values[ca1.t] = 1 * h + 50/60 * h
values[ca0.pos.x] = 0 * km
values[ca01.v_av.x] = 105 * km / h

display_equations_(eqs, values, ca1.pos.x)

solve_and_display_(eqs, values, want=ca1.pos.x)
# ----------------------------------------------------------------------
eqs += kinematics_fundamental(cb, axes=['x'])

eqs += eq_flat(
    ca1.pos.x,
    cb1.pos.x,
)

values[cb0.t] = 0 * h
values[cb0.pos.x] = 0 * km
values[cb01.v_av.x] = 70 * km / h

display_equations_(eqs, values, cb1.t)
solve_and_display_(eqs, values, want=cb1.t)
# cb_1_t = (cb_0_t*v_av_x_cb_0_1 - cb_0_x + cb_1_x)/v_av_x_cb_0_1
# cb_1_t = 2.75*hour

