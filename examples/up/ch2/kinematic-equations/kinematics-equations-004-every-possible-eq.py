
import sympy as sp
from combine_equations.display_equations import display_equation_, display_equations_
from combine_equations.misc import multiply_both_sides, divide_both_sides, expand_lhs, expand_rhs, add_both_sides

# ----------------------------------------------------------------------
def solve_subs(eq_a, eq_b, var):

    result = sp.solve(eq_b, var)

    if len(result) == 1:
        return eq_a.subs(var, result[0])

    raise ValueError("Multiple solutions found; cannot substitute uniquely.")

def symbols_in_common(eq_a, eq_b):
    return eq_a.free_symbols.intersection(eq_b.free_symbols)

def isolate_variable(eq, var):
    sol = sp.solve(eq, var)
    if len(sol) == 1:
        # return sol[0]
        return sp.Eq(var, sol[0])
    raise ValueError("Multiple solutions found; cannot isolate uniquely.")
# ----------------------------------------------------------------------
x_1 = sp.symbols('x_1')
x_2 = sp.symbols('x_2')
v_1x = sp.symbols('v_1x')
v_2x = sp.symbols('v_2x')
v_av_x = sp.symbols('v_av_x')
t_1 = sp.symbols('t_1')
t_2 = sp.symbols('t_2')
dt = sp.symbols('dt')
a_x = sp.symbols('a_x')
# ----------------------------------------------------------------------

# eq 2.2
# v_av_x = (x_2 - x_1) / dt

# eq 2.7
# a_x = (v_2x - v_1x) / dt

# eq 2.10
# v_av_x = (v_1x + v_2x) / 2

# tmp_1 = solve_subs(eq_2_2, eq_2_7, t_2 - t_1)
# v_av_x = a_x*(-x_1 + x_2)/(-v_1x + v_2x)

# tmp_2 = solve_subs(eq_2_2, eq_2_10, v_av_x)
# v_1x/2 + v_2x/2 = (-x_1 + x_2)/(-t_1 + t_2)

# tmp_3 = solve_subs(tmp_1, eq_2_10, v_av_x)
# v_1x/2 + v_2x/2 = a_x*(-x_1 + x_2)/(-v_1x + v_2x)

# tmp_5 = solve_subs(tmp_2, eq_2_7, v_2x)
# a_x*dt/2 + v_1x = (-x_1 + x_2)/dt
#
# tmp = isolate_variable(tmp_5, x_2)
# x_2 = a_x*dt**2/2 + dt*v_1x + x_1

# tmp_2.solve_subs(eq_2_7, v_2x).isolate(x_2)

# ----------------------------------------------------------------------
eq_2_2 = sp.Eq(v_av_x, (x_2 - x_1) / dt)

eq_2_7 = sp.Eq(a_x, (v_2x - v_1x) / dt)

eq_2_10 = sp.Eq(v_av_x, (v_1x + v_2x) / 2)



eqs = []

symbols = symbols_in_common(eq_2_2, eq_2_7)
for symbol in symbols:
    print(f'Solving for {symbol}')
    eqs.append(solve_subs(eq_2_2, eq_2_7, symbol))

# eq = eqs[0]

for eq in eqs.copy():
    symbols = symbols_in_common(eq, eq_2_10)
    for symbol in symbols:
        print(f'Solving for {symbol}')
        eqs.append(solve_subs(eq, eq_2_10, symbol))

display_equations_(eqs)


# ----------------------------------------------------------------------
def derive_all_equations(base_equations, max_depth=2):
    """
    Systematically derive all possible equations from base equations.
    
    Strategy:
    1. For each pair of equations
    2. Find their common symbols
    3. Solve one for each common symbol and substitute into the other
    4. Add new (unique) equations to the set
    5. Repeat with newly derived equations up to max_depth
    """
    
    all_equations = set(base_equations)  # Use set to avoid duplicates
    new_equations = set(base_equations)
    
    for depth in range(max_depth):
        current_round = []
        
        # Try all pairs of equations (including new ones)
        for eq_a in all_equations:
            for eq_b in all_equations:
                if eq_a == eq_b:
                    continue
                
                # Find common symbols
                common = symbols_in_common(eq_a, eq_b)
                
                # Try substituting each common symbol
                for symbol in common:
                    try:
                        # Solve eq_b for symbol, substitute into eq_a
                        new_eq = solve_subs(eq_a, eq_b, symbol)
                        new_eq = sp.simplify(new_eq)
                        
                        # Check if this is truly new (not just algebraically equivalent)
                        if not is_equivalent_to_any(new_eq, all_equations):
                            current_round.append(new_eq)
                    except:
                        pass  # Some substitutions may fail
        
        if not current_round:
            break  # No new equations found
        
        new_equations = set(current_round)
        all_equations.update(new_equations)
        
        print(f"Depth {depth + 1}: Found {len(current_round)} new equations")
    
    return list(all_equations)


def is_equivalent_to_any(eq, equation_set):
    """Check if eq is algebraically equivalent to any equation in the set."""
    for existing_eq in equation_set:
        # Check if difference between equations simplifies to 0
        if sp.simplify(eq.lhs - eq.rhs - (existing_eq.lhs - existing_eq.rhs)) == 0:
            return True
    return False
# ----------------------------------------------------------------------

derive_all_equations([eq_2_2, eq_2_7, eq_2_10], max_depth=3)


















tmp_1 = solve_subs(eq_2_2, eq_2_7, dt)
display_equation_(tmp_1)
# v_av_x = a_x*(-x_1 + x_2)/(-v_1x + v_2x)

tmp = solve_subs(eq_2_2, eq_2_10, v_av_x)
tmp = multiply_both_sides(tmp, dt)
tmp = sp.simplify(tmp)
tmp = multiply_both_sides(tmp, -1)
display_equation_(tmp)
# Same as eq 2.14 from the book.

tmp = isolate_variable(eq_2_7, v_2x)
display_equation_(tmp)
# This is equation 2.8 from the book.

tmp = solve_subs(eq_2_2, eq_2_7, dt)
tmp = solve_subs(tmp, eq_2_10, v_av_x)
tmp = multiply_both_sides(tmp, (-v_1x + v_2x))
tmp = multiply_both_sides(tmp, 2)
tmp = sp.simplify(tmp)
tmp = add_both_sides(tmp, v_1x**2)
display_equation_(tmp)
# 2*a_x*(-x_1 + x_2) + v_1x**2 = v_2x**2
# This is eq 2.13 from the book.

tmp = solve_subs(eq_2_2, eq_2_10, v_av_x)
tmp = solve_subs(tmp, eq_2_7, v_2x)
tmp = isolate_variable(tmp, x_2)
display_equation_(tmp)
# a_x*dt/2 + v_1x = (-x_1 + x_2)/dt
# This is eq 2.12 from the book.

# eq_2_2
#     .subs(eq_2_10.solve_for(v_av_x))
#     .subs(eq_2_7.solve_for(v_2x))
#     .isolate(x_2)




symbols_in_common(eq_2_2, eq_2_7)
symbols_in_common(eq_2_2, eq_2_10)
symbols_in_common(eq_2_7, eq_2_10)

