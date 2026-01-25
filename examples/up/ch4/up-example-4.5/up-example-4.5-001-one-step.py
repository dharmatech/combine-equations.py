
# A waitress shoves a ketchup bottle with mass 0.45 kg 
# to her right
# along a smooth, level lunch counter.
# 
# The bottle leaves her hand moving at 2.0 m/s,
# then slows down as it slides because of a constant horizontal
# friction force exerted on it by the countertop.
# 
# It slides for 1.0 m before coming to rest.
# 
# What are the magnitude and direction 
# of the friction force acting on the bottle?

# ----------------------------------------------------------------------

from pprint import pprint
import sympy as sp

from combine_equations.kinematics_states import *
from combine_equations.solve_system import *
from combine_equations.display_equations import display_equations_
from combine_equations.solve_and_display import solve_and_display_
from combine_equations.misc import eq_flat
from combine_equations.newtons_laws import *

# ----------------------------------------------------------------------

b = make_states_model('b', 2)  # bottle

b0, b1 = b.states

b01 = b.edges[0]

eqs = kinematics_fundamental(b, axes=['x'])

display_equations_(eqs)
# dt_b_0_1 = -b_0_t + b_1_t
# v_av_x_b_0_1 = (-b_0_x + b_1_x)/dt_b_0_1
# a_x_b_0_1 = (-b_0_v_x + b_1_v_x)/dt_b_0_1
# v_av_x_b_0_1 = b_0_v_x/2 + b_1_v_x/2
# ----------------------------------------------------------------------
values = {}

values[b0.t] = 0
values[b0.pos.x] = 0
values[b1.pos.x] = 1.0  # m
values[b0.vel.x] = 2.0  # m/s
values[b1.vel.x] = 0.0  # m/s
# ----------------------------------------------------------------------

# forces: normal, weight, friction

n = make_point("n")  # normal force
w = make_point("w")  # weight
f = make_point("f")  # friction force

m = sp.symbols("m")  # mass
a = make_point("a")  # acceleration

eqs += newtons_second_law([n, w, f], m, a)

eqs += eq_flat(
    a.x, b01.a.x
)

values[n.x] = 0
values[w.x] = 0
values[m]   = 0.45  # kg

display_equations_(eqs, values, want=f.x)
# dt_b_0_1 = -b_0_t + b_1_t
# v_av_x_b_0_1 = (-b_0_x + b_1_x)/dt_b_0_1
# a_x_b_0_1 = (-b_0_v_x + b_1_v_x)/dt_b_0_1
# v_av_x_b_0_1 = b_0_v_x/2 + b_1_v_x/2
# f_x + n_x + w_x = m*a_x
# f_y + n_y + w_y = m*a_y
# a_x = a_x_b_0_1

solve_and_display_(eqs, values, want=f.x)
# f_x = (b_0_v_x**2*m/2 - b_0_x*n_x - b_0_x*w_x - b_1_v_x**2*m/2 + b_1_x*n_x + b_1_x*w_x)/(b_0_x - b_1_x)
# f_x = -0.900000000000000



