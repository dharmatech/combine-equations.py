
from dataclasses import dataclass
from typing import Any

import sympy as sp

from combine_equations.misc import *
from combine_equations.solve_system import solve_system_2
from combine_equations.display_equations import display_equation_
from combine_equations.display_equations import display_equations_
from combine_equations.eliminate_variable_subst import eliminate_variable_subst

# ----------------------------------------------------------------------
# region library
# ----------------------------------------------------------------------

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

# endregion
# -----------------------------------------------------------------------

# ----------------------------------------------------------------------
# region build equations
# ----------------------------------------------------------------------
values_a = {}

# A motorcyclist heading east through a small town
# accelerates at a constant 4.0 m/s^2
# after he leaves the city limits.

m_01 = make_obj_interval('m', 0, 1)
m_0 = m_01.obj_0
m_1 = m_01.obj_1

values_a[m_01.a] = 4 # m/s^2

# At time t = 0
# he is 5.0 m east of the city-limits signpost
# while he moves east at 15 m/s. 

values_a[m_0.x]  =  5 # m
values_a[m_0.v] = 15 # m/s

# (a) Find his position and velocity at t = 2.0 s. 

values_a[m_1.t]    =  2 # s

equations = [
    eq_avg_velocity(m_01),
    eq_acceleration(m_01),
    eq_avg_velocity_2(m_01)
]

equations.append(sp.Eq(m_0.t, 0))

# ----------------------------------------------------------------------
# endregion
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
# region solve
# ----------------------------------------------------------------------

# (a) Find his position and velocity at t = 2.0 s. 

# find x_2

display_equations_(equations, values_a, want=m_1.x)

# region output
# v_av_m_0_1 = (m_1_x - m_0_x)/(m_1_t - m_0_t)
# m_a = (-m_0_v + m_1_v)/(m_1_t - m_0_t)
# v_av_m_0_1 = m_0_v/2 + m_1_v/2
# m_0_t = 0
# endregion

tmp_a = solve_system_2(equations, values_a, m_1.x)
display_equation_(tmp_a)
# m_1_x = m_0_v*m_1_t + m_0_x + m_1_t**2*m_a/2
display_equation_(tmp_a.subs(values_a)) # m_1_x = 43

# Find velocity at t = 2.0 s
tmp_b = solve_system_2(equations, values_a, m_1.v)
display_equation_(tmp_b) # m_1_v = m_0_v + m_1_t*m_a
display_equation_(tmp_b.subs(values_a)) # m_1_v = 23

# ----------------------------------------------------------------------
# (b) Where is he when his speed is 25 m/s?

values_b = values_a.copy()
del(values_b[m_1.t])
values_b[m_1.v] = 25 # m/s

# find x_2

display_equations_(equations, values_b, want=m_1.x)

tmp_c = solve_system_2(equations, values_b, m_1.x)

display_equation_(tmp_c, values_b, want=m_1.x)
# m_1_x = (-m_0_v**2 + 2*m_0_x*m_a + m_1_v**2)/(2*m_a)
display_equation(tmp_c.subs(values_b)) # m_1_x = 55

# ----------------------------------------------------------------------
# endregion
# ----------------------------------------------------------------------