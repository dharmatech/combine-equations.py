
# Three professional wrestlers are fighting over a champion’s belt.
#
# Figure 4.7a shows the horizontal force each wrestler applies 
# to the belt, as viewed from above.
# 
# The forces have magnitudes 
#
# F1 = 50 N
# F2 = 120 N
# F3 = 250 N
# 
# Find the x- and y-components 
# of the net force on the belt, 
# and find its magnitude and direction.

import sympy as sp

from combine_equations.kinematics_states import Point3
from combine_equations.misc import eq_flat

from combine_equations.display_equations import display_equations_

from combine_equations.eliminate_variable_subst import eliminate_variable_subst

# F1 = Point3.make("F1")



# F1.mag = sp.symbols("F1_mag")

# F1 = Point3(
#     x = sp.symbols("F1_x"),
#     y = sp.symbols("F1_y"),
#     z = sp.symbols("F1_z"),

#     mag = sp.symbols("F1_mag"),
#     angle=sp.symbols("F1_angle")
# )

def make_force(prefix: str) -> Point3:
    return Point3(
        x = sp.symbols(f"{prefix}_x"),
        y = sp.symbols(f"{prefix}_y"),
        z = sp.symbols(f"{prefix}_z"),

        mag = sp.symbols(f"{prefix}_mag"),
        angle=sp.symbols(f"{prefix}_angle")
    )

F1 = make_force("F1")
F2 = make_force("F2")
F3 = make_force("F3")

R  = make_force("R") # net force

eqs = []

eqs += eq_flat(
    R.x, F1.x + F2.x + F3.x,
    R.y, F1.y + F2.y + F3.y,

    F1.x, F1.mag * sp.cos(F1.angle),
    F1.y, F1.mag * sp.sin(F1.angle),

    F2.x, F2.mag * sp.cos(F2.angle),
    F2.y, F2.mag * sp.sin(F2.angle),

    F3.x, F3.mag * sp.cos(F3.angle),
    F3.y, F3.mag * sp.sin(F3.angle),

    R.x, R.mag * sp.cos(R.angle),
    R.y, R.mag * sp.sin(R.angle),

    R.mag, sp.sqrt(R.x**2 + R.y**2),
    R.angle, sp.atan2(R.y, R.x)
)

display_equations_(eqs)

tmp = eqs

tmp, _ = eliminate_variable_subst(eqs, F1.x)
tmp, _ = eliminate_variable_subst(tmp, F1.y)

tmp, _ = eliminate_variable_subst(tmp, F2.x)
tmp, _ = eliminate_variable_subst(tmp, F2.y)

tmp, _ = eliminate_variable_subst(tmp, F3.x)
tmp, _ = eliminate_variable_subst(tmp, F3.y)

display_equations_(tmp)

values = {}

values[F1.mag] = 50
values[F1.angle] = sp.rad(0)

values[F2.mag] = 120
values[F2.angle] = sp.rad(270)

values[F3.mag] = 250
values[F3.angle] = sp.rad(180 - 53)

display_equations_(tmp, values)

# for eq in tmp:
#     eq.subs(values)

# tmp = [eq.subs(values) for eq in tmp]

# display_equations_(tmp, values)

from combine_equations.solve_and_display import solve_and_display_

solve_and_display_(tmp, values, R.x)
# R_x = F1_mag*cos(F1_angle) + F2_mag*cos(F2_angle) + F3_mag*cos(F3_angle)
# R_x = -100.453755788012

solve_and_display_(tmp, values, R.y)
# R_y = F1_mag*sin(F1_angle) + F2_mag*sin(F2_angle) + F3_mag*sin(F3_angle)
# R_y = 79.6588775118232

solve_and_display_(tmp, values, R.mag)
# R_mag = sqrt(F1_mag**2 + 2*F1_mag*F2_mag*cos(F1_angle - F2_angle) + 2*F1_mag*F3_mag*cos(F1_angle - F3_angle) + F2_mag**2 + 2*F2_mag*F3_mag*cos(F2_angle - F3_angle) + F3_mag**2)
# R_mag = 128.204889993952

solve_and_display_(tmp, values, R.angle)
# R_angle = atan2(F1_mag*sin(F1_angle) + F2_mag*sin(F2_angle) + F3_mag*sin(F3_angle), F1_mag*cos(F1_angle) + F2_mag*cos(F2_angle) + F3_mag*cos(F3_angle))
# R_angle = 2.47114041353915



