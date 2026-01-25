
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
from combine_equations.solve_and_display import solve_and_display_
from combine_equations.solve_system import solve_with_elimination_attempts

# ----------------------------------------------------------------------
def make_force(prefix: str) -> Point3:
    return Point3(
        x = sp.symbols(f"{prefix}_x"),
        y = sp.symbols(f"{prefix}_y"),
        z = sp.symbols(f"{prefix}_z"),

        mag = sp.symbols(f"{prefix}_mag"),
        angle=sp.symbols(f"{prefix}_angle")
    )
# ----------------------------------------------------------------------

F1 = make_force("F1")
F2 = make_force("F2")
F3 = make_force("F3")

R  = make_force("R") # net force

def force_equations(force: Point3):
    return eq_flat(
        force.x, force.mag * sp.cos(force.angle),
        force.y, force.mag * sp.sin(force.angle),

        force.mag, sp.sqrt(force.x**2 + force.y**2),
        force.angle, sp.atan2(force.y, force.x),
    )

def polar_to_components(force: Point3):
    return eq_flat(
        force.x, force.mag * sp.cos(force.angle),
        force.y, force.mag * sp.sin(force.angle),
    )

def components_to_polar(force: Point3):
    return eq_flat(
        force.mag, sp.sqrt(force.x**2 + force.y**2),
        force.angle, sp.atan2(force.y, force.x),
    )

def superposition_equations(R: Point3, forces: list[Point3]):
    eqs = []

    eqs += eq_flat(
        R.x, sum(f.x for f in forces),
        R.y, sum(f.y for f in forces)
    )

    return eqs

    # eqs = []
    # for coord in ['x', 'y', 'z']:
    #     eqs += eq_flat(
    #         getattr(R, coord),
    #         sum(getattr(f, coord) for f in forces)
    #     )
    # return eqs

eqs = []

eqs += superposition_equations(R, [F1, F2, F3])

eqs += polar_to_components(F1)
eqs += polar_to_components(F2)
eqs += polar_to_components(F3)

eqs += components_to_polar(R)

display_equations_(eqs)

values = {}

values[F1.mag] = 50
values[F1.angle] = sp.rad(0)

values[F2.mag] = 120
values[F2.angle] = sp.rad(270)

values[F3.mag] = 250
values[F3.angle] = sp.rad(180 - 53)

display_equations_(eqs, values)
# R_x = F1_x + F2_x + F3_x
# R_y = F1_y + F2_y + F3_y
# F1_x = F1_mag*cos(F1_angle)
# F1_y = F1_mag*sin(F1_angle)
# F2_x = F2_mag*cos(F2_angle)
# F2_y = F2_mag*sin(F2_angle)
# F3_x = F3_mag*cos(F3_angle)
# F3_y = F3_mag*sin(F3_angle)
# R_mag = sqrt(R_x**2 + R_y**2)
# R_angle = atan2(R_y, R_x)

# ----------------------------------------------------------------------
tmp = eqs

tmp, _ = eliminate_variable_subst(tmp, F1.x)
tmp, _ = eliminate_variable_subst(tmp, F2.x)
tmp, _ = eliminate_variable_subst(tmp, F3.x)

display_equations_(tmp, values)

# ----------------------------------------------------------------------

tmp, _ = eliminate_variable_subst(tmp, F1.y)
tmp, _ = eliminate_variable_subst(tmp, F2.y)
tmp, _ = eliminate_variable_subst(tmp, F3.y)

display_equations_(tmp, values)

# F1_mag*cos(F1_angle) = -F2_mag*cos(F2_angle) - F3_mag*cos(F3_angle) + R_x         1
# F1_mag*sin(F1_angle) = -F2_mag*sin(F2_angle) - F3_mag*sin(F3_angle) + R_y         2
# R_mag = sqrt(R_x**2 + R_y**2)                                                     3
# R_angle = atan2(R_y, R_x)                                                         4


# At this point, it seems straightfoward.
#
# Solve 1 for R_x. Substitute into 3 and 4.
# Solve 2 for R_y. Substitute into 3 and 4.

# However, if I elim R_x:

tmp, _ = eliminate_variable_subst(tmp, R.x)

# we get this:

display_equations_(tmp, values)
# F1_mag*cos(F1_angle) = -F2_mag*cos(F2_angle) - F3_mag*cos(F3_angle) + sqrt((R_mag - R_y)*(R_mag + R_y))
# F1_mag*sin(F1_angle) = -F2_mag*sin(F2_angle) - F3_mag*sin(F3_angle) + R_y
# R_mag = sqrt(R_mag**2)
# R_angle = atan2(R_y, sqrt((R_mag - R_y)*(R_mag + R_y)))



tmp, _ = eliminate_variable_subst(tmp, R.x)
tmp, _ = eliminate_variable_subst(tmp, R.y)

display_equations_(tmp, values)







# solve_with_elimination_attempts(eqs, values, R.x)

solve_and_display_(eqs, values, R.x, version=2)
# Elimination attempts elapsed: 87.460s
# R_x = F1_mag*cos(F1_angle) + F2_mag*cos(F2_angle) + F3_mag*cos(F3_angle)
# R_x = -100.453755788012

solve_and_display_(eqs, values, R.y, version=2)
# Elimination attempts elapsed: 223.839s
# R_y = F1_mag*sin(F1_angle) + F2_mag*sin(F2_angle) + F3_mag*sin(F3_angle)
# R_y = 79.6588775118232

solve_and_display_(eqs, values, R.mag, version=2)
# Elimination attempts elapsed: 1m 43.41s
# R_mag = sqrt(R_x**2 + R_y**2)
# R_mag = (R_x**2 + R_y**2)**0.5

# R_mag = sqrt(F1_mag**2 + 2*F1_mag*F2_mag*cos(F1_angle - F2_angle) + 2*F1_mag*F3_mag*cos(F1_angle - F3_angle) + F2_mag**2 + 2*F2_mag*F3_mag*cos(F2_angle - F3_angle) + F3_mag**2)
# R_mag = 128.204889993952

solve_and_display_(eqs, values, R.angle, version=2)
# R_angle = atan2(F1_mag*sin(F1_angle) + F2_mag*sin(F2_angle) + F3_mag*sin(F3_angle), F1_mag*cos(F1_angle) + F2_mag*cos(F2_angle) + F3_mag*cos(F3_angle))
# R_angle = 2.47114041353915

solve_and_display_(eqs, values, R_angle_deg)
# R_angle_deg = 180*atan2(F1_mag*sin(F1_angle) + F2_mag*sin(F2_angle) + F3_mag*sin(F3_angle), F1_mag*cos(F1_angle) + F2_mag*cos(F2_angle) + F3_mag*cos(F3_angle))/pi
# R_angle_deg = 141.585916280006

