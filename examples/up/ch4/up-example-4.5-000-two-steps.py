
# A waitress shoves a ketchup bottle with mass 0.45 kg 
# to her right
# along a smooth, level lunch counter.
# 
# The bottle leaves her hand moving at 2.0 m/s,
# then slows down as it slides because of a constant horizontal
# friction force exerted on it by the countertop.
# 
# It slides for 1.0 m before coming to rest.
# 
# What are the magnitude and direction 
# of the friction force acting on the bottle?

# ----------------------------------------------------------------------

from pprint import pprint
import sympy as sp

from combine_equations.kinematics_states import (
    make_states_model,
    kinematics_fundamental,
    magnitude_and_angle_equations,
)

from combine_equations.kinematics_states import State
from combine_equations.solve_system import *
from combine_equations.display_equations import display_equations_
from combine_equations.eliminate_variable_subst import eliminate_zero_eqs
from combine_equations.solve_and_display import solve_and_display_
from combine_equations.misc import eq_flat
# ----------------------------------------------------------------------

from combine_equations.kinematics_states import Point3

def make_point(prefix: str) -> Point3:
    return Point3(
        x = sp.symbols(f"{prefix}_x"),
        y = sp.symbols(f"{prefix}_y"),
        z = sp.symbols(f"{prefix}_z"),

        mag = sp.symbols(f"{prefix}_mag"),
        angle=sp.symbols(f"{prefix}_angle")
    )

def superposition_equations(R: Point3, forces: list[Point3]):
    eqs = []

    eqs += eq_flat(
        R.x, sum(f.x for f in forces),
        R.y, sum(f.y for f in forces)
    )

    return eqs

def newtons_second_law(forces: list[Point3], mass: sp.Symbol, acceleration: Point3):
    # F = m*a
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

b = make_states_model('b', 2)  # bottle

b0, b1 = b.states

b01 = b.edges[0]

eqs = kinematics_fundamental(b, axes=['x'])

display_equations_(eqs)
# ----------------------------------------------------------------------

# eqs += eq_flat(
#     b0.t,    0,
#     b0.pos.x, 0,

# )

values = {}

values[b0.t] = 0
values[b0.pos.x] = 0
values[b1.pos.x] = 1.0  # m
values[b0.vel.x] = 2.0  # m/s
values[b1.vel.x] = 0.0  # m/s
# ----------------------------------------------------------------------
# display_equations_(eqs, values, want=b01.a.x)

# tmp = eqs

# tmp, _ = eliminate_variable_subst(tmp, b01.dt)
# tmp, _ = eliminate_variable_subst(tmp, b1.t)
# tmp, _ = eliminate_variable_subst(tmp, b01.v_av.x)

# display_equations_(tmp, values, want=b01.a.x)

solve_and_display_(eqs, values, want=b01.a.x)
# a_x_b_0_1 = (b_0_v_x - b_1_v_x)*(b_0_v_x + b_1_v_x)/(2*(b_0_x - b_1_x))
# a_x_b_0_1 = -2.00000000000000

# ----------------------------------------------------------------------

# forces: normal, weight, friction

n = make_point("n")  # normal force
w = make_point("w")  # weight
f = make_point("f")  # friction force

m = sp.symbols("m")  # mass
a = make_point("a")  # acceleration

eqs_2 = newtons_second_law([n, w, f], m, a)

values[n.x] = 0
values[w.x] = 0
values[m]   = 0.45  # kg

display_equations_(eqs_2, values, want=f.x)