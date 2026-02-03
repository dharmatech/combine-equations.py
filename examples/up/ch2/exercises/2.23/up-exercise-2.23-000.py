# Automobile Airbags.
# 
# The human body 
# can survive an acceleration trauma incident 
# (sudden stop) 
# if the magnitude of the acceleration
# is less than 250 m/s^2. 
# 
# If you are in an automobile accident
# with an initial speed of 105 km/h (65 mi/h)
# and are stopped by an airbag that inflates from the dashboard,
# over what minimum distance must
# the airbag stop you for you to survive the crash?
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
from combine_equations.equation_gui import show_equation_gui
# ----------------------------------------------------------------------
b = make_states_model("b", 2)  # body
b0, b1 = b.states
b01 = b.edges[0]
eqs = kinematics_fundamental(b, axes=['x'])
# ----------------------------------------------------------------------
values = {}
values[b01.a.x] = -250 * m/s**2
values[b0.vel.x] = 105 * km/h
values[b1.vel.x] = 0   * m/s
values[b0.t]     = 0   * s
values[b0.pos.x] = 0   * m
# ----------------------------------------------------------------------
display_equations_(eqs, values, want=b1.pos.x)
# dt_b_0_1 = -b_0_t + b_1_t
# v_av_x_b_0_1 = (b_1_x - b_0_x)/dt_b_0_1
# a_x_b_0_1 = (-b_0_v_x + b_1_v_x)/dt_b_0_1
# v_av_x_b_0_1 = b_0_v_x/2 + b_1_v_x/2
solve_and_display_(eqs, values, want=b1.pos.x)
# b_1_x = (2*a_x_b_0_1*b_0_x - b_0_v_x**2 + b_1_v_x**2)/(2*a_x_b_0_1)
# b_1_x = 22.05*kilometer**2*second**2/(hour**2*meter)

# unit conversion