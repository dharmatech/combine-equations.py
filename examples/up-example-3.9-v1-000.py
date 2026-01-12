
# You throw a ball from your window 8.0 m above the ground.
#
# When the ball leaves your hand, 
# it is moving at 10.0 m/s 
# at an angle of 20.0° below the horizontal.
# 
# How far horizontally from your window will the
# ball hit the ground? Ignore air resistance.
# ----------------------------------------------------------------------

from pprint import pprint
import sympy as sp

from combine_equations.kinematics_states import (
    make_states_model,
    kinematics_fundamental,
)

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

def solve_and_display_(equations, values, want, check_knowns=True):
    
    tmp = solve_system_multiple_solutions(equations, values, want, check_knowns=check_knowns)
    
    for index, sol in enumerate(tmp):
        if len(tmp) > 1:
            print(f"Solution {index+1}:")
        display_equation_(sol, values, want=want)
        # display_equation_(sol.subs(values), values, want=want)
        display_equation_(sp.N(sol.subs(values)), values, want=want)

from combine_equations.kinematics_states import State

def magnitude_and_angle_equations(obj: State) -> list:
    eqs = eq_flat(
        obj.vel.x,    obj.vel.mag*sp.cos(obj.vel.angle),
        obj.vel.y,    obj.vel.mag*sp.sin(obj.vel.angle),

        obj.vel.mag,   sp.sqrt(obj.vel.x**2 + obj.vel.y**2),
        obj.vel.angle, sp.atan2(obj.vel.y, obj.vel.x)
    )

    return eqs        
# ----------------------------------------------------------------------

b = make_states_model('b', 2)

b0, b1 = b.states

b01 = b.edges[0]

eqs = kinematics_fundamental(b, axes=['x', 'y'])

display_equations_(eqs)

# ----------------------------------------------------------------------
# projectile motion

g = sp.symbols('g')

# You throw a ball from your window 8.0 m above the ground.

eqs += eq_flat(
    b0.pos.x, 0,
    # b0.pos.y, 8.0,

    b01.a.x, 0,
    b01.a.y, -g,

    b0.t, 0,

    b0.vel.x, b1.vel.x,

    b1.pos.y, 0 # hits ground
)

eqs = eliminate_zero_eqs(eqs)

display_equations_(eqs)
# ----------------------------------------------------------------------

values = {}

values[g] = 9.81 # m/s^2

values[b0.pos.y] = 8.0 # m

# When the ball leaves your hand, 
# it is moving at 10.0 m/s 
# at an angle of 20.0° below the horizontal.

eqs += magnitude_and_angle_equations(b0)

values[b0.vel.mag] = 10.0 # m/s
values[b0.vel.angle] = sp.N(sp.rad(-20.0)) # degrees to radians
# ----------------------------------------------------------------------
# How far horizontally from your window will the
# ball hit the ground? Ignore air resistance.
# ----------------------------------------------------------------------
# If we use the solver directly, it reports no solutions found.
display_equations_(eqs, values, want=b1.pos.x)
# b_1_t = dt_b_0_1
# v_av_x_b_0_1 = b_1_x/dt_b_0_1
# v_av_y_b_0_1 = -b_0_y/dt_b_0_1
# (-b_0_v_x + b_1_v_x)/dt_b_0_1 = 0
# a_y_b_0_1 = (-b_0_v_y + b_1_v_y)/dt_b_0_1
# b_0_v_x = -b_1_v_x + 2*v_av_x_b_0_1
# b_0_v_y = -b_1_v_y + 2*v_av_y_b_0_1
# a_y_b_0_1 = -g
# b_0_v_x = b_1_v_x
# b_0_v_x = b_0_v_mag*cos(b_0_v_angle)
# b_0_v_y = b_0_v_mag*sin(b_0_v_angle)
# b_0_v_mag = sqrt(b_0_v_x**2 + b_0_v_y**2)
# b_0_v_angle = atan2(b_0_v_y, b_0_v_x)
solve_and_display_(eqs, values, want=b1.pos.x)
# ValueError: No solutions found.
# ----------------------------------------------------------------------
# If we manually eliminate variables, we can eventually get the solution.
tmp = eqs

# tmp, _ = eliminate_variable_subst(tmp, b01.dt)
tmp, _ = eliminate_variable_subst(tmp, b01.v_av.x)
tmp, _ = eliminate_variable_subst(tmp, b01.v_av.y)
tmp, _ = eliminate_variable_subst(tmp, b01.a.y)
tmp, _ = eliminate_variable_subst(tmp, b0.vel.x)
tmp, _ = eliminate_variable_subst(tmp, b0.vel.y)
tmp, _ = eliminate_variable_subst(tmp, b1.vel.x)
tmp, _ = eliminate_variable_subst(tmp, b1.vel.y)
tmp, _ = eliminate_variable_subst(tmp, b1.t)

display_equations_([tmp[0]], values, want=b1.pos.x)
# b_0_v_mag*sin(b_0_v_angle) = b_1_x*g/(b_0_v_mag*cos(b_0_v_angle)) - b_0_v_mag*sin(2*b_0_v_angle)/(2*cos(b_0_v_angle)) - 2*b_0_v_mag*b_0_y*cos(b_0_v_angle)/b_1_x
solve_and_display_([tmp[0]], values, want=b1.pos.x)
# Solving for unknowns: [b_1_x]
# Solution 1:
# b_1_x = b_0_v_mag*(b_0_v_mag*sin(b_0_v_angle) - sqrt(b_0_v_mag**2*sin(b_0_v_angle)**2 + 2*b_0_y*g))*cos(b_0_v_angle)/g
# b_1_x = -15.7161745661753
# Solution 2:
# b_1_x = b_0_v_mag*(b_0_v_mag*sin(b_0_v_angle) + sqrt(b_0_v_mag**2*sin(b_0_v_angle)**2 + 2*b_0_y*g))*cos(b_0_v_angle)/g
# b_1_x = 9.16380341748480
# ----------------------------------------------------------------------
# If we eliminate variables until we're down to 3 equations,
# we still get an error.
# However, interestingly, the first equations can be solved for b1.pos.x.
# We in fact do so above.

display_equations_(tmp, values, want=b1.pos.x)
# b_0_v_mag*sin(b_0_v_angle) = b_1_x*g/(b_0_v_mag*cos(b_0_v_angle)) - b_0_v_mag*sin(2*b_0_v_angle)/(2*cos(b_0_v_angle)) - 2*b_0_v_mag*b_0_y*cos(b_0_v_angle)/b_1_x
# b_0_v_mag = sqrt(b_0_v_mag**2)
# b_0_v_angle = atan2(b_0_v_mag*sin(b_0_v_angle), b_0_v_mag*cos(b_0_v_angle))
solve_and_display_(tmp, values, want=b1.pos.x, check_knowns=False)
# IndexError: Index out of range: a[1]
# ----------------------------------------------------------------------

# equations = tmp
# want = b1.pos.x


display_equations_([tmp[1]], values)

sp.simplify([tmp[1]])

sp.simplify(sp.sqrt(b1.t**2))

tmp[1].free_symbols

# Drop any equations whose free symbols don’t intersect the unknowns;
# if they simplify to False, error out as inconsistent.

tmp[2].free_symbols

x = sp.symbols('x', real=True, positive=True)
x = sp.symbols('x', positive=True)
x = sp.symbols('x', real=True)
x = sp.symbols('x')

sp.sqrt(x**2)







display_equations_(tmp, values, want=b1.pos.x)
eqs = tmp

display_equations_(eqs, values, want=b1.pos.x)
solve_and_display_(eqs, values, want=b1.pos.x)

display_equation_(eqs[0], values)

sp.solve(eqs[0], b1.t)

solve_and_display_([eqs[0]], values, want=b1.t)
# Solving for unknowns: [b_1_t]
#
# Solution 1:
# b_1_t = (b_0_v_mag*sin(b_0_v_angle) - sqrt(b_0_v_mag**2*sin(b_0_v_angle)**2 + 2*b_0_y*g))/g
# b_1_t = -1.67248036416750
#
# Solution 2:
# b_1_t = (b_0_v_mag*sin(b_0_v_angle) + sqrt(b_0_v_mag**2*sin(b_0_v_angle)**2 + 2*b_0_y*g))/g
# b_1_t = 0.975191590822613


# sp.Eq(b_0_v_angle, atan2(b_1_t*g + b_1_v_y, b_1_x/b_1_t))

# sp.simplify(sp.Eq(b0.vel.angle, sp.atan2(b1.t*g + b1.vel.y, b1.pos.x/b1.t)))

# sp.simplify(sp.Eq(1, sp.atan2(b1.t, 2/b1.t)))



# a = sp.symbols('a')

# sp.simplify(sp.Eq(1, sp.atan2(a, 2/a)))




