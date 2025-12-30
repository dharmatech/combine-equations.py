
from combine_equations.misc import combine_equations_sp
from combine_equations.misc import isolate_variable

def solve_system(equations, values, want):
    knowns = list(values.keys())
    tmp = equations[0]
    for eq in equations[1:]:
        elim_candidates = tmp.free_symbols.intersection(eq.free_symbols)
        elim_candidates = elim_candidates.difference(knowns).difference({want})
        if not elim_candidates:
            raise ValueError("No suitable variable to eliminate found.")
        elim = elim_candidates.pop()
        tmp = combine_equations_sp(tmp, eq, elim)
    return isolate_variable(tmp, want)





def solve_system_alt(equations, values, want):

    knowns = list(values.keys())

    def check(eq, want):
        eq_has_want = want in eq.free_symbols

        eq_can_solve = eq.free_symbols.difference(knowns).difference({want}) == set()

        return eq_has_want and eq_can_solve
    
    tmp = next((eq for eq in equations if check(eq, want)), None)

    if tmp is not None:
        tmp = solve_system([tmp], values, want=want)
        return tmp
        
    tmp = equations[0]
    for eq in equations[1:]:
        elim_candidates = tmp.free_symbols.intersection(eq.free_symbols)
        elim_candidates = elim_candidates.difference(knowns).difference({want})
        if not elim_candidates:
            raise ValueError("No suitable variable to eliminate found.")
        elim = elim_candidates.pop()
        tmp = combine_equations_sp(tmp, eq, elim)
    return isolate_variable(tmp, want)



import sympy as sp

def connected_unknowns(equations, values, want):
    knowns = set(values.keys())
    eqs = [eq.subs(values) for eq in equations]

    needed = {want}
    changed = True

    while changed:
        changed = False
        for eq in eqs:
            unknowns_in_eq = eq.free_symbols - knowns
            if unknowns_in_eq & needed:
                new_needed = needed | unknowns_in_eq
                if new_needed != needed:
                    needed = new_needed
                    changed = True

    return needed  # includes want


def solve_system_2(equations, values, want):

    unknowns = connected_unknowns(equations, values, want)

    unknowns = list(unknowns)

    result = sp.solve(equations, unknowns, dict=True)
    
    return sp.Eq(want, result[0][want])
