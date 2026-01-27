
# A 2.45*10^4 N truck traveling in the +x-direction makes an emergency stop;
# the x-component of the net external force acting on it is -1.83*10^4 N.
# 
# What is its acceleration?
# ----------------------------------------------------------------------
from pprint import pprint
import sympy as sp

from sympy.physics.units import newton, meter, second, meters

from combine_equations.kinematics_states import *
from combine_equations.solve_system import *
from combine_equations.display_equations import display_equations_
from combine_equations.solve_and_display import solve_and_display_
from combine_equations.misc import eq_flat
from combine_equations.newtons_laws import *
# ----------------------------------------------------------------------
w = sp.symbols("w")  # weight
m = sp.symbols("m")  # mass
g = sp.symbols("g")  # gravity

F_x = sp.symbols("F_x")  # net force
a_x = sp.symbols("a_x")  # acceleration
# ----------------------------------------------------------------------
eqs = eq_flat(
    w,   m * g,
    F_x, m * a_x,
)
# ----------------------------------------------------------------------
values = {}

values[w]   =  2.45e4 * newton
values[F_x] = -1.83e4 * newton
values[g]   =  9.81   * meter/second**2
# ----------------------------------------------------------------------
display_equations_(eqs, values, want=a_x)
# w = g*m
# F_x = a_x*m

solve_and_display_(eqs, values, want=a_x)
# a_x = F_x*g/w
# a_x = -7.3274693877551*meter/second**2