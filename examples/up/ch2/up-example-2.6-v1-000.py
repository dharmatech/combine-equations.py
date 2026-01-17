
# A one-euro coin is dropped from the Leaning Tower of Pisa and falls
# freely from rest. What are its position and velocity after 1.0 s, 2.0 s, and
# 3.0 s? Ignore air resistance.

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

# -----------------------------------------------------------------------
# endregion
# -----------------------------------------------------------------------

# ----------------------------------------------------------------------
# region build equations
# ----------------------------------------------------------------------

# A one-euro coin is dropped from the Leaning Tower of Pisa and falls
# freely from rest.

c_01 = make_obj_interval('c', 0, 1)
c_0 = c_01.obj_0
c_1 = c_01.obj_1

equations = [
    eq_avg_velocity(c_01),
    eq_acceleration(c_01),
    eq_avg_velocity_2(c_01),
]

display_equations_(equations)

equations.append(sp.Eq(c_0.t, 0))
equations.append(sp.Eq(c_0.v, 0))
equations.append(sp.Eq(c_0.x, 0))

# ----------------------------------------------------------------------
# endregion
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
# region solve
# ----------------------------------------------------------------------

values = {}

values[c_01.a] = 9.8  # m/s^2

# What are its position and velocity after 1.0 s, 2.0 s, and
# 3.0 s? Ignore air resistance.

values[c_1.t] = 1.0  # s
tmp_a = solve_system_2(equations, values=values, want=c_1.x)
display_equation_(tmp_a, values, want=c_1.x) # c_1_x = c_1_t**2*c_a/2
display_equation_(tmp_a.subs(values), values, want=c_1.x) # c_1_x = 4.90

tmp_a = solve_system_2(equations, values=values, want=c_1.v)
display_equation_(tmp_a, values, want=c_1.v) # c_1_v = c_1_t*c_a
display_equation_(tmp_a.subs(values), values, want=c_1.v) # c_1_v = 9.8


values[c_1.t] = 2.0  # s
tmp_a = solve_system_2(equations, values=values, want=c_1.x)
display_equation_(tmp_a, values, want=c_1.x) # c_1_x = c_1_t**2*c_a/2
display_equation_(tmp_a.subs(values), values, want=c_1.x) # c_1_x = 19.6

values[c_1.t] = 3.0  # s
tmp_a = solve_system_2(equations, values=values, want=c_1.x)
display_equation_(tmp_a, values, want=c_1.x) # c_1_x = c_1_t**2*c_a/2
display_equation_(tmp_a.subs(values), values, want=c_1.x) # c_1_x = 44.1


# ----------------------------------------------------------------------
# endregion 
# ----------------------------------------------------------------------