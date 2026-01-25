
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

import sympy as sm
import sympy.physics.mechanics as me


N = me.ReferenceFrame('N')

O = me.Point('O')

t = me.dynamicsymbols._t

O.set_vel(N, 0)

B = me.Point('B')

x, ux = me.dynamicsymbols('x ux')

B.set_pos(O, x * N.x)

B.set_vel(N, ux * N.x)

m = sm.symbols('m')

bottle = me.Particle('bottle', B, m)

bodies = [bottle]

mu = sm.symbols('mu')

g = sm.symbols('g')

forces = (B, -mu * m * g * N.x)

FL = [forces]

kd = sm.Matrix([ux - x.diff(t)])

kane = me.KanesMethod(N, q_ind=[x], u_ind=[ux], kd_eqs=kd)

fr, frstar = kane.kanes_equations(bodies, FL)

force = kane.forcing_full

MM = kane.mass_matrix_full

sm.pprint(MM)

sm.pprint(force)
# >>> sm.pprint(force)
# ⎡  ux(t) ⎤
# ⎢        ⎥
# ⎣ -g⋅m⋅μ  ⎦







# f_x = (b_0_v_x**2*m/2)/(b_1_x)

# f_x = -b_0_v_x**2*m/(2*b_1_x)