from pprint import pprint
import sympy as sp

from combine_equations.kinematics_states import (
    make_states_model,
    kinematics_fundamental,
)

from combine_equations.solve_system import solve_system_2
from combine_equations.display_equations import display_equation_
from combine_equations.display_equations import display_equations_


# A motorist traveling at a constant 15 m/s passes a school crossing.
# A police officer starts from rest with constant acceleration 3.0 m/s^2.
# (a) time until officer passes motorist
# (b) officer speed at that time
# (c) distance traveled (both) at that time


# ----------------------------------------------------------------------
# Build models + fundamental equations
# ----------------------------------------------------------------------

# Two-state models: state 0 -> state 1 for each object
m = make_states_model("m", 2, include_v_av=True)  # motorist
p = make_states_model("p", 2, include_v_av=True)  # police

pprint(m)

# region output
# >>> pprint(m)
# StatesModel(states=[State(pos=Point3(x=m_0_x, y=m_0_y, z=m_0_z),
#                           vel=Point3(x=m_0_v_x, y=m_0_v_y, z=m_0_v_z),
#                           t=m_0_t),
#                     State(pos=Point3(x=m_1_x, y=m_1_y, z=m_1_z),
#                           vel=Point3(x=m_1_v_x, y=m_1_v_y, z=m_1_v_z),
#                           t=m_1_t)],
#             edges=[EdgeVars(dt=dt_m_0_1,
#                             a=Point3(x=a_x_m_0_1, y=a_y_m_0_1, z=a_z_m_0_1),
#                             v_av=Point3(x=v_av_x_m_0_1,
#                                         y=v_av_y_m_0_1,
#                                         z=v_av_z_m_0_1))])
# endregion

pprint(p)

# region output
# >>> pprint(p)
# StatesModel(states=[State(pos=Point3(x=p_0_x, y=p_0_y, z=p_0_z),
#                           vel=Point3(x=p_0_v_x, y=p_0_v_y, z=p_0_v_z),
#                           t=p_0_t),
#                     State(pos=Point3(x=p_1_x, y=p_1_y, z=p_1_z),
#                           vel=Point3(x=p_1_v_x, y=p_1_v_y, z=p_1_v_z),
#                           t=p_1_t)],
#             edges=[EdgeVars(dt=dt_p_0_1,
#                             a=Point3(x=a_x_p_0_1, y=a_y_p_0_1, z=a_z_p_0_1),
#                             v_av=Point3(x=v_av_x_p_0_1,
#                                         y=v_av_y_p_0_1,
#                                         z=v_av_z_p_0_1))])
# endregion

m0, m1 = m.states[0], m.states[1]
p0, p1 = p.states[0], p.states[1]

m01 = m.edges[0]
p01 = p.edges[0]

# Fundamental equations (EQ2/EQ7/EQ10) in 1D-x, plus dt definitions
eqs = []
eqs += kinematics_fundamental(m, axes=("x",), include_dt_defs=True)
eqs += kinematics_fundamental(p, axes=("x",), include_dt_defs=True)

display_equations_(eqs)

# region output
# >>> display_equations_(eqs)
# dt_m_0_1 = -m_0_t + m_1_t
# v_av_x_m_0_1 = (-m_0_x + m_1_x)/dt_m_0_1
# a_x_m_0_1 = (-m_0_v_x + m_1_v_x)/dt_m_0_1
# v_av_x_m_0_1 = m_0_v_x/2 + m_1_v_x/2
# dt_p_0_1 = -p_0_t + p_1_t
# v_av_x_p_0_1 = (-p_0_x + p_1_x)/dt_p_0_1
# a_x_p_0_1 = (-p_0_v_x + p_1_v_x)/dt_p_0_1
# v_av_x_p_0_1 = p_0_v_x/2 + p_1_v_x/2
# endregion

# ----------------------------------------------------------------------
# Constraints + values from the story
# ----------------------------------------------------------------------

values = {}

# Motorist constant speed: introduce m_v and tie both endpoint velocities to it
m_v = sp.Symbol("m_v")
eqs.append(sp.Eq(m0.vel.x, m_v)) # m0vx = m_v
eqs.append(sp.Eq(m1.vel.x, m_v)) # m1vx = m_v
values[m_v] = 15

# Officer starts from rest at the signpost (x=0) at t=0
eqs.append(sp.Eq(p0.vel.x, 0)) # p0vx = 0
eqs.append(sp.Eq(p0.pos.x, 0)) # p0x  = 0

# Both start at the signpost at t=0
eqs.append(sp.Eq(m0.pos.x, 0))
eqs.append(sp.Eq(m0.t, 0))
eqs.append(sp.Eq(p0.t, 0))

# Officer acceleration is constant 3.0 m/s^2 on interval 0->1
values[p01.a.x] = 3

pprint(p01)

# Catch-up condition at state 1: same position, same time
dist = sp.Symbol("dist")
t_01 = sp.Symbol("t_01")

eqs.append(sp.Eq(dist, m1.pos.x))
eqs.append(sp.Eq(dist, p1.pos.x))

eqs.append(sp.Eq(t_01, m1.t))
eqs.append(sp.Eq(t_01, p1.t))

# ----------------------------------------------------------------------
# Solve
# ----------------------------------------------------------------------

# (a) time until officer passes motorist
display_equations_(eqs, values, want=t_01)
sol_t = solve_system_2(eqs, values, want=t_01)
display_equation_(sol_t)                 # t_01 = 2*m_v/a_x_p_0_1
display_equation_(sol_t.subs(values))    # t_01 = 10

# (b) officer speed at that time
display_equations_(eqs, values, want=p1.vel.x)
sol_v = solve_system_2(eqs, values, want=p1.vel.x)
display_equation_(sol_v)                 # p_1_v_x = 2*m_v
display_equation_(sol_v.subs(values))    # p_1_v_x = 30

# (c) distance traveled
display_equations_(eqs, values, want=dist)
sol_dist = solve_system_2(eqs, values, want=dist)
display_equation_(sol_dist)              # dist = 2*m_v**2/a_x_p_0_1
display_equation_(sol_dist.subs(values)) # dist = 150
