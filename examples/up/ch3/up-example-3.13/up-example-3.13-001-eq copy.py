
# You drive north on a straight two-lane road at a constant 88 km/h.
# 
# A truck in the other lane approaches you at a constant 104 km/h (Fig. 3.33).
# 
# Find 
# 
# (a) the truck’s velocity relative to you and 
# 
# (b) your velocity relative to the truck.
# 
# (c) How do the relative velocities change after you and the
# truck pass each other?
# 
# Treat this as a one-dimensional problem.

import sympy as sp

from combine_equations.kinematics_states import *
from combine_equations.solve_system import *
from combine_equations.display_equations import display_equations_
from combine_equations.solve_and_display import solve_and_display_
from combine_equations.misc import eq_flat
from combine_equations.newtons_laws import *

from sympy.physics.units import km, h

# ------------------------------------------------------------------------------

v_YE = sp.symbols('v_YE')  # your velocity relative to earth
v_TE = sp.symbols('v_TE')  # truck's velocity relative to earth
v_TY = sp.symbols('v_TY')  # truck's velocity relative to you
v_YT = sp.symbols('v_YT')  # your velocity relative to truck

# ------------------------------------------------------------------------------

eqs = eq_flat(
    v_TE,    v_TY + v_YE,
    v_YT,   -v_TY
)

# v_YE = v_YT + v_TE

# v_TY = v_TE - v_YE

display_equations_(eqs)
    
# ------------------------------------------------------------------------------

values = {}

values[v_YE] =   88 * km/h
values[v_TE] = -104 * km/h

# ------------------------------------------------------------------------------

# (a) the truck’s velocity relative to you and 

solve_and_display_(eqs, values, want=v_TY)
# v_TY = v_TE - v_YE
# v_TY = -192.0*kilometer/hour

# (b) your velocity relative to the truck.

solve_and_display_(eqs, values, want=v_YT)
# v_YT = -v_TE + v_YE
# v_YT = 192.0*kilometer/hour
