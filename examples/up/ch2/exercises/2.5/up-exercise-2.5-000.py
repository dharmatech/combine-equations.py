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
# From section 2.2 page 38

# “Velocity” and “speed” are used interchangeably in everyday language,
# but they have distinct definitions in physics.
# 
# We use the term speed to denote 
# distance traveled divided by time, 
# on either an average or an instantaneous basis.
# 
# Instantaneous speed, 
# for which we use the symbol v with no subscripts,
# measures how fast a particle is moving; 
# 
# instantaneous velocity 
# measures how fast and in what direction it’s moving. 
# 
# Instantaneous speed is the magnitude of instantaneous velocity
# and so can never be negative.
# 
# For example, 
# a particle with instantaneous velocity v_x = 25 m/s
# and a second particle with v_xx = -25 m/s
# are moving in opposite directions at the same instantaneous speed 25 m/s.

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
p = make_states_model("p", 3)  # person

p0, p1, p2 = p.states

p01 = p.edges[0]
p12 = p.edges[1]

eqs = []

eqs += kinematics_fundamental(p, axes=['x'])

# dx_p_0_1 = p_1_x - p_0_x
# dx_p_1_2 = p_2_x - p_1_x
# dx_p_0_2 = p_2_x - p_0_x

dx_p_0_1 = sp.Symbol("dx_p_0_1")
dx_p_1_2 = sp.Symbol("dx_p_1_2")
dx_p_0_2 = sp.Symbol("dx_p_0_2")

eqs += eq_flat(
    dx_p_0_1, p1.pos.x - p0.pos.x,
    dx_p_1_2, p2.pos.x - p1.pos.x,
    dx_p_0_2, p2.pos.x - p0.pos.x,
)

# average velocity for entire trip

# (p_2_x - p_0_x) / (p_2_t - p_0_t)

# average speed for entire trip

# abs(dx_p_0_1) + abs(dx_p_1_2) / (p_2_t - p_0_t)

speed_01 = sp.Symbol("speed_01")
speed_12 = sp.Symbol("speed_12")
speed_02 = sp.Symbol("speed_02")

avg_speed_02 = sp.Symbol("avg_speed_02")


# ----------------------------------------------------------------------
values = {}

# values[p0.t] = 0 * s
# values[p1.t] = 28.0 * s
# values[p2.t] = values[p1.t] + 36.0 * s

# values[p0.pos.x] = 0 * m
# values[p1.pos.x] = 60.0 * m

values[p0.t] = 0 * s

values[p01.dt] = 28.0 * s
values[p12.dt] = 36.0 * s

values[dx_p_0_1] =  60.0 * m
values[dx_p_1_2] = -40.0 * m

values[p0.pos.x] = 0 * m

display_equations_(eqs, values, want=avg_speed_02)
# ----------------------------------------------------------------------

# average velocity for entire trip

# avg_vel_02 = (p_2_x - p_0_x) / (p_2_t - p_0_t)

avg_vel_02 = sp.Symbol("avg_vel_02")

eqs += eq_flat(
    avg_vel_02, (p2.pos.x - p0.pos.x) / (p2.t - p0.t),
)

tmp = eqs
tmp, _ = eliminate_variable_subst(tmp, p2.pos.x)
tmp, _ = eliminate_variable_subst(tmp, p1.pos.x)
tmp, _ = eliminate_variable_subst(tmp, p2.t)
tmp, _ = eliminate_variable_subst(tmp, p1.t)

display_equations_(tmp, values, want=avg_vel_02)

solve_and_display_(eqs, values, want=avg_vel_02)
# avg_vel_02 = (dx_p_0_1 + dx_p_1_2)/(dt_p_0_1 + dt_p_1_2)
# avg_vel_02 = 0.3125*meter/second



display_equations_(eqs, values, want=avg_vel_02)

# ----------------------------------------------------------------------
eqs += eq_flat(
    # speed_01, sp.Abs( dx_p_0_1 ) / p01.dt,
    # speed_12, sp.Abs( dx_p_1_2 ) / p12.dt,
    # speed_02, speed_01 + speed_12,

    avg_speed_02, (sp.Abs( dx_p_0_1 ) + sp.Abs( dx_p_1_2 )) / (p2.t - p0.t),    
)

tmp = eqs
tmp, _ = eliminate_variable_subst(tmp, p2.t)
tmp, _ = eliminate_variable_subst(tmp, p1.t)

display_equations_(tmp, values, want=avg_speed_02)

solve_and_display_(eqs, values, want=avg_speed_02)
# avg_speed_02 = (Abs(dx_p_0_1) + Abs(dx_p_1_2))/(dt_p_0_1 + dt_p_1_2)
# avg_speed_02 = 1.5625*meter/second
# ----------------------------------------------------------------------