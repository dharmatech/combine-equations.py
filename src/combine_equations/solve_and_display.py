
import sympy as sp
from combine_equations.solve_system import *
from combine_equations.display_equations import display_equation_

def solve_and_display_(equations, values, want, version=1, return_solutions=False):
    
    if version == 1:
        tmp = solve_system_multiple_solutions(equations, values, want)
    elif version == 0:
        tmp = solve_system_multiple_solutions_000(equations, values, want)
    elif version == 2:
        tmp = solve_with_elimination_attempts(equations, values, want)
    else:
        raise ValueError(f"Unsupported version: {version}")
    
    for index, sol in enumerate(tmp):
        if len(tmp) > 1:
            print(f"Solution {index+1}:")
        display_equation_(sol, values, want=want)
        # display_equation_(sol.subs(values), values, want=want)
        display_equation_(sp.N(sol.subs(values)), values, want=want)
        
    if return_solutions:

        solutions = []

        for sol in tmp:
            symbolic = sol
            numeric = sp.N(sol.subs(values))
            solutions.append([symbolic, numeric])

        return solutions

