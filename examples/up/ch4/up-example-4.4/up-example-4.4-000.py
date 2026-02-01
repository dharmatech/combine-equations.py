
# A worker applies a constant horizontal force 
# with magnitude 20 N 
# to a box with mass 40 kg 
# resting on a level, 
# freshly waxed floor with negligible friction. 
# 
# What is the acceleration of the box?

# ----------------------------------------------------------------------

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

def make_point(prefix: str) -> Point3:
    return Point3(
        x = sp.symbols(f"{prefix}_x"),
        y = sp.symbols(f"{prefix}_y"),
        z = sp.symbols(f"{prefix}_z"),

        mag = sp.symbols(f"{prefix}_mag"),
        angle=sp.symbols(f"{prefix}_angle")
    )


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

def newtons_second_law(forces: list[Point3], mass: sp.Symbol, acceleration: Point3):
    eqs = []
    # for coord in ['x', 'y']:
    #     eqs += eq_flat(
    #         sum(getattr(f, coord) for f in forces),
    #         mass * getattr(acceleration, coord)
    #     )

    eqs += eq_flat(
        sum(f.x for f in forces),    mass * acceleration.x,
        sum(f.y for f in forces),    mass * acceleration.y,
    )

    return eqs

# ----------------------------------------------------------------------

F  = make_force("F") # force applied by worker
n = make_force("n")  # normal force
w = make_force("w")  # weight
m = sp.symbols("m")  # mass
a = make_point("a")  # acceleration

eqs = []

eqs += newtons_second_law([F, n, w], m, a)

display_equations_(eqs)

values = {}

values[F.x] = 20  # N
values[F.y] = 0   # N

values[a.y] = 0   # m/s²

values[n.x] = 0   # N
values[w.x] = 0   # N

values[m] = 40    # kg

display_equations_(eqs, values, want=a.x)

from combine_equations.eliminate_variable_subst import eliminate_zero_eqs

eqs = eliminate_zero_eqs(eqs)

display_equations_(eqs, values, want=a.x)

solve_and_display_(eqs, values, want=a.x)
# a_x = (F_x + n_x + w_x)/m
# a_x = 0.500000000000000

