import sympy as sp

from combine_equations.kinematics_states import (
    make_states_model,
    kinematics_fundamental,
)

from combine_equations.solve_system import solve_system_2
from combine_equations.display_equations import display_equation_
from combine_equations.display_equations import display_equations_

# ----------------------------------------------------------------------
def solve_and_display(equations, values, want):
    tmp = solve_system_2(equations, values, want)
    display_equation_(tmp, want=want)
    display_equation_(tmp.subs(values), want=want)
    return tmp
# ----------------------------------------------------------------------
# Build model + equations
# ----------------------------------------------------------------------

# Create a 2-state model: state 0 -> state 1
# include_v_av=True because we want the EQ2/EQ10 avg-velocity formulation
m = make_states_model("m", 2, include_v_av=True)

m0 = m.states[0]
m1 = m.states[1]
e01 = m.edges[0]  # edge variables for interval 0->1

# Build the fundamental equations (EQ2, EQ7, EQ10) for 1D along x,
# plus dt definition equations to avoid sign-flip clutter.
equations = []
equations += kinematics_fundamental(
    m,
    axes=("x",),
    include_dt_defs=True,
    include_eq2=True,
    include_eq7=True,
    include_eq10=True,
)

display_equations_(equations)

# Initial time constraint: t0 = 0
equations.append(sp.Eq(m0.t, 0))


# ----------------------------------------------------------------------
# Values for part (a)
# ----------------------------------------------------------------------

values_a = {}

# Constant acceleration after leaving city limits: a = 4.0 m/s^2
# In this library, acceleration is edge-level:
values_a[e01.a.x] = 4

# At time t = 0: x0 = 5 m, v0 = 15 m/s
values_a[m0.pos.x] = 5
values_a[m0.vel.x] = 15

# At t = 2 s: t1 = 2
values_a[m1.t] = 2

# ----------------------------------------------------------------------
# (a) Find position and velocity at t = 2.0 s
# ----------------------------------------------------------------------

display_equations_(equations, values_a, want=m1.pos.x)

tmp_a = solve_and_display(equations, values_a, m1.pos.x)  # should be 43
tmp_b = solve_and_display(equations, values_a, m1.vel.x)  # should be 23

# ----------------------------------------------------------------------
# (b) Where is he when his speed is 25 m/s?
# ----------------------------------------------------------------------

values_b = values_a.copy()
del values_b[m1.t]           # unknown time
values_b[m1.vel.x] = 25      # speed at state 1

display_equations_(equations, values_b, want=m1.pos.x)

tmp_c = solve_and_display(equations, values_b, m1.pos.x)  # should be 55