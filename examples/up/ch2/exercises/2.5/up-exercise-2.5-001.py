# Starting from the front door of a ranch house, 
# you walk 60.0 m due east to a windmill, 
# turn around, 
# and then slowly walk 40.0 m west to a bench, 
# where you sit and watch the sunrise.
# 
# It takes you 28.0 s to walk from the house to the windmill 
# and then 36.0 s to walk from the windmill to the bench.
# 
# For the entire trip from the front door to the
# bench, what are your 
# 
# (a) average velocity and 
# 
# (b) average speed?
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
dx_p_0_1 = sp.Symbol("dx_p_0_1")
dx_p_1_2 = sp.Symbol("dx_p_1_2")

avg_speed_02 = sp.Symbol("avg_speed_02")
avg_vel_02   = sp.Symbol("avg_vel_02")
# ----------------------------------------------------------------------
p = make_states_model("p", 3)  # person

p0, p1, p2 = p.states

p01 = p.edges[0]
p12 = p.edges[1]

eqs = []

eqs += kinematics_fundamental(p, axes=['x'])

eqs += eq_flat(
    dx_p_0_1, p1.pos.x - p0.pos.x,
    dx_p_1_2, p2.pos.x - p1.pos.x,    

    avg_speed_02, (sp.Abs( dx_p_0_1 ) + sp.Abs( dx_p_1_2 )) / (p2.t - p0.t),    

    avg_vel_02,   (p2.pos.x - p0.pos.x) / (p2.t - p0.t),
)
# ----------------------------------------------------------------------
values = {}

values[p0.t] = 0 * s

values[p01.dt] = 28.0 * s
values[p12.dt] = 36.0 * s

values[dx_p_0_1] =  60.0 * m
values[dx_p_1_2] = -40.0 * m

values[p0.pos.x] = 0 * m
# ----------------------------------------------------------------------
solve_and_display_(eqs, values, want=avg_vel_02)
# avg_vel_02 = (dx_p_0_1 + dx_p_1_2)/(dt_p_0_1 + dt_p_1_2)
# avg_vel_02 = 0.3125*meter/second

solve_and_display_(eqs, values, want=avg_speed_02)
# avg_speed_02 = (Abs(dx_p_0_1) + Abs(dx_p_1_2))/(dt_p_0_1 + dt_p_1_2)
# avg_speed_02 = 1.5625*meter/second
# ----------------------------------------------------------------------