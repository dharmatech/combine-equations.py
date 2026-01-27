
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

from dataclasses import dataclass
from typing import Any

import sympy as sp

from combine_equations.misc import *
from combine_equations.solve_system import solve_system_2
from combine_equations.display_equations import display_equation_
from combine_equations.display_equations import display_equations_
from combine_equations.eliminate_variable_subst import eliminate_variable_subst

@dataclass(frozen=True)
class Obj:
        
    x: Any
    t: Any
    v: Any
    a: Any

def make_obj(prefix):
    x = sp.symbols(f'{prefix}_x')
    t = sp.symbols(f'{prefix}_t')
    v = sp.symbols(f'{prefix}_v')
    a = sp.symbols(f'{prefix}_a')
    return Obj(x, t, v, a)

@dataclass(frozen=True)
class Interval:
    obj_0: Obj
    obj_1: Obj
    v_av: sp.Symbol
    a: sp.Symbol

def eq_avg_velocity(I: Interval):
    return sp.Eq(I.v_av, (I.obj_1.x - I.obj_0.x) / (I.obj_1.t - I.obj_0.t))

def eq_acceleration(I: Interval):
    return sp.Eq(I.a, (I.obj_1.v - I.obj_0.v) / (I.obj_1.t - I.obj_0.t))

def eq_avg_velocity_2(I: Interval):
    return sp.Eq(I.v_av, (I.obj_0.v + I.obj_1.v) / 2)

def substitute(equations, values):
    return [eq.subs(values) for eq in equations]

# -----------------------------------------------------------------------

# m_0 = make_obj('m_0')
# m_1 = make_obj('m_1')

# m_01 = Interval(m_0, m_1, sp.symbols('v_av_m_0_1'), sp.symbols('m_a'))

def make_obj_interval(prefix, point_a, point_b):
    obj_a = make_obj(f'{prefix}_{point_a}')
    obj_b = make_obj(f'{prefix}_{point_b}')
    v_av = sp.symbols(f'v_av_{prefix}_{point_a}_{point_b}')
    a = sp.symbols(f'{prefix}_a')
    return Interval(obj_a, obj_b, v_av, a)

# -----------------------------------------------------------------------
# Library part complete.
# Example part starts.
# -----------------------------------------------------------------------

m_01 = make_obj_interval('m', 0, 1)
m_0 = m_01.obj_0
m_1 = m_01.obj_1

p_01 = make_obj_interval('p', 0, 1)
p_0 = p_01.obj_0
p_1 = p_01.obj_1

# region consider
# m.s[0].x
# m.s[0].v
# m.s[0].a
# m.s[0].t
# endregion

equations = [
    eq_avg_velocity(m_01),
    eq_acceleration(m_01),
    eq_avg_velocity_2(m_01),

    eq_avg_velocity(p_01),
    eq_acceleration(p_01),
    eq_avg_velocity_2(p_01)
]

# A motorist traveling at a constant 15 m/s
#
# Instead of m_0.v == m_1.v
# let's do:
# m_0.v == m_v
# m_1.v == m_v
#
# Then we can eliminate m_0.v and m_1.v
# and only have m_v

m_v = sp.symbols('m_v')

equations.append(sp.Eq(m_0.v, m_v))
equations.append(sp.Eq(m_1.v, m_v))

display_equations_(equations)

#region output
# v_av_m_0_1 = (-m_0_x + m_1_x)/(-m_0_t + m_1_t)
# m_a = (-m_0_v + m_1_v)/(-m_0_t + m_1_t)
# v_av_m_0_1 = m_0_v/2 + m_1_v/2
# v_av_p_0_1 = (-p_0_x + p_1_x)/(-p_0_t + p_1_t)
# p_a = (-p_0_v + p_1_v)/(-p_0_t + p_1_t)
# v_av_p_0_1 = p_0_v/2 + p_1_v/2
# m_0_v = m_v
# m_1_v = m_v
#endregion

values = {}

values[m_v] = 15

tmp = equations
tmp, replacement = eliminate_variable_subst(tmp, m_0.v)
tmp, replacement = eliminate_variable_subst(tmp, m_1.v)

display_equations_(tmp)

# region output
# v_av_m_0_1 = (m_0_x - m_1_x)/(m_0_t - m_1_t)
# m_a = 0
# m_v = v_av_m_0_1
# v_av_p_0_1 = (p_0_x - p_1_x)/(p_0_t - p_1_t)
# p_a = (p_0_v - p_1_v)/(p_0_t - p_1_t)
# p_0_v = -p_1_v + 2*v_av_p_0_1
# endregion

tmp, replacement = eliminate_variable_subst(tmp, m_01.a)
tmp, replacement = eliminate_variable_subst(tmp, m_01.v_av)

display_equations_(tmp)

# region output
# m_v = (m_0_x - m_1_x)/(m_0_t - m_1_t)
# v_av_p_0_1 = (p_0_x - p_1_x)/(p_0_t - p_1_t)
# p_a = (p_0_v - p_1_v)/(p_0_t - p_1_t)
# p_0_v = -p_1_v + 2*v_av_p_0_1
# endregion

# Just as the motorist passes the school-crossing sign,
# a police officer on a motorcycle stopped there
# starts in pursuit with constant acceleration 3.0 m/s^2

tmp.append(sp.Eq(p_0.v, 0)) # initial velocity is 0
tmp.append(sp.Eq(p_0.x, 0)) # initial position is 0

tmp, replacement = eliminate_variable_subst(tmp, p_0.v)
tmp, replacement = eliminate_variable_subst(tmp, p_0.x)

display_equations_(tmp)

# region output
# m_v = (m_0_x - m_1_x)/(m_0_t - m_1_t)
# v_av_p_0_1 = -p_1_x/(p_0_t - p_1_t)
# p_a = -p_1_v/(p_0_t - p_1_t)
# p_1_v = 2*v_av_p_0_1
# endregion

tmp.append(sp.Eq(m_0.t, 0)) # initial time is 0
tmp.append(sp.Eq(p_0.t, 0)) # initial time is 0

tmp, replacement = eliminate_variable_subst(tmp, m_0.t)
tmp, replacement = eliminate_variable_subst(tmp, p_0.t)

display_equations_(tmp)

# region output
# m_v = (-m_0_x + m_1_x)/m_1_t
# v_av_p_0_1 = p_1_x/p_1_t
# p_a = p_1_v/p_1_t
# p_1_v = 2*v_av_p_0_1
# endregion

tmp.append(sp.Eq(m_0.x, 0)) # initial position is 0

tmp, replacement = eliminate_variable_subst(tmp, m_0.x)

display_equations_(tmp)

# region output
# m_v = m_1_x/m_1_t
# v_av_p_0_1 = p_1_x/p_1_t
# p_a = p_1_v/p_1_t
# p_1_v = 2*v_av_p_0_1
# endregion

values[p_01.a] = 3

# (a) How much time elapses before the officer passes the motorist?

# m_1.x == p_1.x

dist = sp.symbols('dist')

tmp.append(sp.Eq(dist, m_1.x))
tmp.append(sp.Eq(dist, p_1.x))

display_equations_(tmp)

tmp, replacement = eliminate_variable_subst(tmp, m_1.x)
tmp, replacement = eliminate_variable_subst(tmp, p_1.x)

display_equations_(tmp)

# region output
# m_v = dist/m_1_t
# v_av_p_0_1 = dist/p_1_t
# p_a = p_1_v/p_1_t
# p_1_v = 2*v_av_p_0_1
# endregion

t_01 = sp.symbols('t_01')

tmp.append(sp.Eq(t_01, m_1.t))
tmp.append(sp.Eq(t_01, p_1.t))

tmp, replacement = eliminate_variable_subst(tmp, m_1.t)
tmp, replacement = eliminate_variable_subst(tmp, p_1.t)

display_equations_(tmp)

# region output
# m_v = dist/t_01
# v_av_p_0_1 = dist/t_01
# p_a = p_1_v/t_01
# p_1_v = 2*v_av_p_0_1
# endregion

display_equations_(tmp, values, want=t_01)

tmp_a = solve_system_2(tmp, values, want=t_01)

display_equation_(tmp_a) # t_01 = 2*m_v/p_a

display_equation_(tmp_a.subs(values)) # t_01 = 10

# At that time,
# (b) what is the officer’s speed and

# officers speed : p_1.v

display_equations_(tmp, values, want=p_1.v)

tmp_b = solve_system_2(tmp, values, want=p_1.v)

display_equation_(tmp_b) # p_1_v = 2*m_v

display_equation_(tmp_b.subs(values)) # p_1_v = 30

# (c) how far has each vehicle traveled?

# distance : dist

display_equations_(tmp, values, want=dist)

tmp_c = solve_system_2(tmp, values, want=dist)

display_equation_(tmp_c) # dist = 2*m_v**2/p_a

display_equation_(tmp_c.subs(values)) # dist = 150




