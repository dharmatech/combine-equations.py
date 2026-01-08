from pprint import pprint
import sympy as sp

from combine_equations.kinematics_states import (
    make_states_model,
    kinematics_fundamental,
)

from combine_equations.solve_system import solve_system_2
from combine_equations.solve_system import solve_system_multiple_solutions
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

def solve_and_display(equations, values, want):
    tmp = solve_system_2(equations, values, want)
    display_equation_(tmp, values, want=want)
    display_equation_(tmp.subs(values), values, want=want)

def solve_and_display_(equations, values, want):
    
    tmp = solve_system_multiple_solutions(equations, values, want)
    
    for index, sol in enumerate(tmp):
        if len(tmp) > 1:
            print(f"Solution {index+1}:")
        display_equation_(sol, values, want=want)
        display_equation_(sol.subs(values), values, want=want)
# ----------------------------------------------------------------------
# A motorcycle stunt rider
# rides off the edge of a cliff.
# 
# Just at the edge
# his velocity is horizontal,
# with magnitude 9.0 m/s.
# 
# Find
# the motorcycle’s position,
# distance from the edge of the cliff,
# and velocity
# 0.50 s after it leaves the edge of the cliff.
# 
# Ignore air resistance.
# ----------------------------------------------------------------------

m = make_states_model('m', 2)

m0, m1 = m.states

m01 = m.edges[0]

eqs = kinematics_fundamental(m, axes=['x', 'y'])

display_equations_(eqs)

# ----------------------------------------------------------------------

# projectile motion

g = sp.symbols('g')

eqs += eq_flat(
    m0.pos.x, 0,
    m0.pos.y, 0,
    
    m01.a.x,  0,
    m01.a.y, -g,

    m0.t, 0,


)

eqs = eliminate_zero_eqs(eqs)

display_equations_(eqs)

values = {}

# Just at the edge
# his velocity is horizontal,
# with magnitude 9.0 m/s.

values[m0.vel.x] = 9.0  # m/s
values[m0.vel.y] = 0.0  # m/s

values[m1.vel.x] = 9.0  # m/s

values[g]        = 9.8  # m/s^2

# Find
# the motorcycle’s position,
# distance from the edge of the cliff,
# and velocity
# 0.50 s after it leaves the edge of the cliff.

values[m1.t] = 0.50  # s

display_equations_(eqs, values)

# ----------------------------------------------------------------------
# Find the motorcycle’s position
# ----------------------------------------------------------------------



solve_and_display_(eqs, values, want=m1.pos.x)
# m_1_x = m_1_t*(m_0_v_x + m_1_v_x)/2
# m_1_x = 4.50000000000000
solve_and_display_(eqs, values, want=m1.pos.y)
# m_1_y = m_1_t*(-g*m_1_t + 2*m_0_v_y)/2
# m_1_y = -1.22500000000000

display_equations_(eqs, values, want=m1.pos.x)

# display_equations_(equations, values, want=want)

# ----------------------------------------------------------------------
# distance from the edge of the cliff
# ----------------------------------------------------------------------

# tmp = sp.sqrt(m1.pos.x**2 + m1.pos.y**2)

dist = sp.symbols('dist')

eqs += eq_flat(
    dist, sp.sqrt(m1.pos.x**2 + m1.pos.y**2)
)

display_equations_(eqs, values, want=dist)

solve_and_display_(eqs, values, want=dist)
# dist = sqrt(m_1_t**2*((m_0_v_x + m_1_v_x)**2 + (g*m_1_t - 2*m_0_v_y)**2))/2
# dist = 4.66375653309647

# ----------------------------------------------------------------------
# velocity
# ----------------------------------------------------------------------

display_equations_(eqs, values)

# m1.vel

# vel_mag = sp.sqrt(m1.vel.x**2 + m1.vel.y**2)
# vel_angle = sp.atan2(m1.vel.y, m1.vel.x)

vel_mag = sp.symbols('vel_mag')
vel_angle = sp.symbols('vel_angle')


eqs += eq_flat(
    vel_mag, sp.sqrt(m1.vel.x**2 + m1.vel.y**2),
    vel_angle, sp.atan2(m1.vel.y, m1.vel.x)
)

display_equations_(eqs, values, want=vel_mag)

solve_and_display_(eqs, values, want=vel_mag)
# vel_mag = sqrt(m_1_v_x**2 + (g*m_1_t - m_0_v_y)**2)
# vel_mag = 10.2474387043788

display_equations_(eqs, values, want=vel_angle)
solve_and_display_(eqs, values, want=vel_angle)
# vel_angle = atan2(-g*m_1_t + m_0_v_y, m_1_v_x)
# vel_angle = -0.498567905638218

vel_angle_deg = sp.symbols('vel_angle_deg')

eqs += eq_flat(
    vel_angle_deg, vel_angle * 180 / sp.pi
)

values[sp.pi] = sp.N(sp.pi)

display_equations_(eqs, values, want=vel_angle_deg)
solve_and_display_(eqs, values, want=vel_angle_deg)
# vel_angle_deg = 180*atan2(-g*m_1_t + m_0_v_y, m_1_v_x)/pi
# vel_angle_deg = -28.5658367937466

