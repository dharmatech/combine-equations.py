
# A monkey escapes from the zoo and climbs a tree.
# 
# After failing to entice the monkey down, 
# the zookeeper fires a tranquilizer dart 
# directly at the monkey (Fig. 3.26).
# 
# The monkey lets go 
# at the instant the dart leaves the gun.
# 
# Show that
# the dart will always hit the monkey, 
# provided that
# the dart reaches the monkey before he hits the ground and runs away.

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

d = make_states_model('d', 2)  # dart

d0, d1 = d.states

d01 = d.edges[0]

eqs_d = kinematics_fundamental(d, axes=['x', 'y'])

eqs_d += magnitude_and_angle_equations(d0)

display_equations_(eqs_d)

D = sp.symbols('D')  # horizontal distance to monkey
# ----------------------------------------------------------------------
# projectile motion

g = sp.symbols('g')

# dart

eqs_d += eq_flat(
    d0.pos.x, 0,
    d0.pos.y, 0,

    d01.a.x, 0,
    d01.a.y, -g,

    d0.t, 0,

    d0.vel.x, d1.vel.x,

    d1.pos.x, D,
)

display_equations_(eqs_d, want=D)

values = {}
values[g] = 9.81  # m/s^2
values[d0.vel.mag] = d0.vel.mag # test value
values[d0.vel.angle] = d0.vel.angle # test value

eqs_d = eliminate_zero_eqs(eqs_d)

display_equations_(eqs_d, values, want=D)

tmp = eqs_d

tmp, _ = eliminate_variable_subst(tmp, d01.dt)
tmp, _ = eliminate_variable_subst(tmp, d01.v_av.x)
tmp, _ = eliminate_variable_subst(tmp, d0.vel.x)
tmp, _ = eliminate_variable_subst(tmp, d1.vel.x)
tmp, _ = eliminate_variable_subst(tmp, d0.vel.y)
tmp, _ = eliminate_variable_subst(tmp, d1.pos.x)

tmp, _ = eliminate_variable_subst(tmp, d01.v_av.y)
tmp, _ = eliminate_variable_subst(tmp, d01.a.y)
tmp, _ = eliminate_variable_subst(tmp, d1.vel.y)


display_equations_(tmp, values, want=D)
display_equations_(tmp, values, want=d1.t)

eq_1 = tmp[0]
eq_2 = tmp[1]

(sp.solve(tmp[1], d1.pos.y)[0]).expand()


from combine_equations.misc import isolate_variable
from combine_equations.display_equations import display_equation_

display_equation_(isolate_variable(tmp[1], d1.pos.y).expand())
# d_1_y = d_0_v_mag*d_1_t*sin(d_0_v_angle) - d_1_t**2*g/2





display_equations_([tmp[1]], values, want=D)
# d_0_v_mag*cos(d_0_v_angle) = D/d_1_t

display_equations_([tmp[0]], values, want=d1.pos.y)


sp.solve(tmp[0], d1.pos.y)

sp.expand(sp.solve(tmp[0], d1.pos.y)[0])


# sp.expand(sp.solve(tmp[0], d1.pos.y))


# eq_1 = tmp[1]

# -----------------------------------------------------------------------
# monkey
# -----------------------------------------------------------------------

m = make_states_model('m', 2)  # monkey

m0, m1 = m.states

m01 = m.edges[0]

eqs_m = kinematics_fundamental(m, axes=['x', 'y'])

display_equations_(eqs_m)
# ----------------------------------------------------------------------

eqs_m += eq_flat(
    m0.pos.x,    D,
    m0.pos.y,    D * sp.tan(d0.vel.angle),

    m01.a.x, 0,
    m01.a.y, -g,

    m0.t, 0,

    m0.vel.x, 0,
    m0.vel.y, 0,

    m1.vel.x, 0
)

display_equations_(eqs_m, want=m1.pos.y)

eqs_m = eliminate_zero_eqs(eqs_m)

display_equations_(eqs_m, want=m1.pos.y)

tmp = eqs_m

tmp, _ = eliminate_variable_subst(tmp, m0.pos.y)
tmp, _ = eliminate_variable_subst(tmp, m01.dt)
tmp, _ = eliminate_variable_subst(tmp, m01.v_av.y)
tmp, _ = eliminate_variable_subst(tmp, m1.vel.y)
tmp, _ = eliminate_variable_subst(tmp, m01.a.y)

display_equations_(tmp, want=m1.pos.y)

display_equations_([tmp[2]])
# D*tan(d_0_v_angle) = g*m_1_t**2/2 + m_1_y

eq_3 = tmp[2]



# ----------------------------------------------------------------------
# D*tan(d_0_v_angle) = g*m_1_t**2/2 + m_1_y
# d_0_v_mag*cos(d_0_v_angle) = D/d_1_t

eqs = [eq_1, eq_2, eq_3]

t = sp.symbols('t')
y = sp.symbols('y')

eqs += eq_flat(
    d1.t, t,
    m1.t, t,

    d1.pos.y, y,
    m1.pos.y, y,    
)

tmp = eqs

tmp, _ = eliminate_variable_subst(tmp, d1.t)
tmp, _ = eliminate_variable_subst(tmp, m1.t)

tmp, _ = eliminate_variable_subst(tmp, d1.pos.y)
tmp, _ = eliminate_variable_subst(tmp, m1.pos.y)

tmp, _ = eliminate_variable_subst(tmp, y)
tmp, _ = eliminate_variable_subst(tmp, t)

display_equations_(tmp, values)
# empty list of equations
