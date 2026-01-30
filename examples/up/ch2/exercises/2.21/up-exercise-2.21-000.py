# A Fast Pitch.
# 
# The fastest measured pitched baseball
# left the pitcher’s hand at a speed of 45.0 m/s.
# 
# If the pitcher was in contact with the ball
# over a distance of 1.50 m 
# and produced constant acceleration,
# 
# (a) what acceleration did he give the ball, and
# 
# (b) how much time did it take him to pitch it?
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
b = make_states_model("b", 2)  # baseball
b0, b1 = b.states
b01 = b.edges[0]
eqs = kinematics_fundamental(b, axes=['x'])
# ----------------------------------------------------------------------
values = {}
values[b0.pos.x] =  0    * m
values[b1.pos.x] =  1.50 * m
values[b0.vel.x] =  0    * m/s
values[b1.vel.x] = 45.0  * m/s
values[b0.t]     =  0    * s
# ----------------------------------------------------------------------
display_equations_(eqs, values, want=b01.a.x)
solve_and_display_(eqs, values, want=b01.a.x)
# a_x_b_0_1 = (b_0_v_x - b_1_v_x)*(b_0_v_x + b_1_v_x)/(2*(b_0_x - b_1_x))
# a_x_b_0_1 = 675.0*meter/second**2
# ----------------------------------------------------------------------
display_equations_(eqs, values, want=b01.dt)
solve_and_display_(eqs, values, want=b01.dt)
# dt_b_0_1 = 2*(-b_0_x + b_1_x)/(b_0_v_x + b_1_v_x)
# dt_b_0_1 = 0.0666666666666667*second
# ----------------------------------------------------------------------

tmp = eqs
tmp, _ = eliminate_variable_subst(tmp, b01.v_av.x)
display_equations_(tmp, values, want=b01.a.x)
# ----------------------------------------------------------------------
# Launch interactive GUI
# Uncomment to open the GUI version:
show_equation_gui(eqs, values, want=b01.a.x, description="Fast Pitch Problem")

show_equation_gui(eqs, values, want=b01.dt, description="Fast Pitch Problem")

