from pprint import pprint
import sympy as sp

from combine_equations.kinematics_states import (
    make_states_model,
    kinematics_fundamental,
)

from combine_equations.solve_system import solve_system_2
from combine_equations.display_equations import display_equation_
from combine_equations.display_equations import display_equations_
from combine_equations.eliminate_variable_subst import eliminate_variable_subst

def eq_flat(*items):
    if len(items) % 2:
        raise ValueError(f"eq_flat needs an even number of items; got {len(items)}")
    return [sp.Eq(items[i], items[i+1]) for i in range(0, len(items), 2)]

# All items in eqs where right rhs is zero.

def eliminate_zero_eqs(equations):
    eqs_zero = [eq for eq in equations if eq.rhs == 0]
    tmp = equations
    for eq in eqs_zero:
        var = eq.lhs
        tmp, _ = eliminate_variable_subst(tmp, var)
    return tmp


# A motorist traveling at a constant 15 m/s
# (54 km/h, or about 34 mi/h)
# passes a school crossing where
# the speed limit is 10 m/s
# (36 km/h, or about 22 mi/h).

# Just as the motorist passes the school-crossing sign,
# a police officer on a motorcycle stopped there
# starts in pursuit with constant acceleration 3.0 m/s^2
# (Fig. 2.21a).

# (a) How much time elapses before the officer passes the motorist?

# At that time,
# (b) what is the officer’s speed and
# (c) how far has each vehicle traveled?

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

m_v  = sp.Symbol("m_v")
dist = sp.Symbol("dist")
t_01 = sp.Symbol("t_01")

eqs += eq_flat(
    m_v,      m0.vel.x, # motorist has constant speed
    m_v,      m1.vel.x,
        
    p0.vel.x, 0, # police officer starts from rest

    # school crossing is 0
    m0.pos.x, 0,
    p0.pos.x, 0,   
        
    m0.t,     0,
    p0.t,     0,
    
    # How much time elapses before the officer passes the motorist?
    # dist is the same for both at that time
    dist, m1.pos.x,
    dist, p1.pos.x,   

    t_01, m1.t,
    t_01, p1.t    
)

# A motorist traveling at a constant 15 m/s
values[m_v] = 15

# Just as the motorist passes the school-crossing sign,
# a police officer on a motorcycle stopped there
# starts in pursuit with constant acceleration 3.0 m/s^2
values[p01.a.x] = 3
# ----------------------------------------------------------------------
display_equations_(eqs, values)

tmp = eliminate_zero_eqs(eqs)

display_equations_(tmp, values) 

# region output
# >>> display_equations_(tmp, values) 
# dt_m_0_1 = m_1_t
# v_av_x_m_0_1 = m_1_x/dt_m_0_1
# a_x_m_0_1 = (-m_0_v_x + m_1_v_x)/dt_m_0_1
# m_0_v_x = -m_1_v_x + 2*v_av_x_m_0_1
# dt_p_0_1 = p_1_t
# v_av_x_p_0_1 = p_1_x/dt_p_0_1
# a_x_p_0_1 = p_1_v_x/dt_p_0_1
# p_1_v_x = 2*v_av_x_p_0_1
# m_0_v_x = m_v
# m_1_v_x = m_v
# dist = m_1_x
# dist = p_1_x
# m_1_t = t_01
# p_1_t = t_01
# endregion

for sym in [m0.vel.x, m1.vel.x, m1.pos.x, p1.pos.x, m1.t, p1.t]:
    tmp, _ = eliminate_variable_subst(tmp, sym)

display_equations_(tmp)

# region output
# >>> display_equations_(tmp)
# v_av_x_m_0_1 = dist/dt_m_0_1
# a_x_m_0_1 = 0
# m_v = v_av_x_m_0_1
# v_av_x_p_0_1 = dist/dt_p_0_1
# a_x_p_0_1 = p_1_v_x/dt_p_0_1
# p_1_v_x = 2*v_av_x_p_0_1
# dt_m_0_1 = t_01
# dt_p_0_1 = t_01
# endregion

eqs = tmp

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
