
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

from sympy.physics.units import km, h

v_YE = sp.symbols('v_YE')  # your velocity relative to earth
v_TE = sp.symbols('v_TE')  # truck's velocity relative to earth

values = {}

values[v_YE] =   88 * km/h
values[v_TE] = -104 * km/h

# (a) the truck’s velocity relative to you and 

v_TY = v_TE - v_YE

v_TY.subs(values) # -192*kilometer/hour

# (b) your velocity relative to the truck.

v_YT = v_YE - v_TE

v_YT.subs(values) # 192*kilometer/hour

