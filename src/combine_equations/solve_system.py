
from combine_equations.misc import combine_equations_sp
from combine_equations.misc import isolate_variable

# def solve_system(equations, values, want):
#     knowns = list(values.keys())
#     tmp = equations[0]
#     for eq in equations[1:]:
#         elim_candidates = tmp.free_symbols.intersection(eq.free_symbols)
#         elim_candidates = elim_candidates.difference(knowns).difference({want})
#         if not elim_candidates:
#             raise ValueError("No suitable variable to eliminate found.")
#         elim = elim_candidates.pop()
#         tmp = combine_equations_sp(tmp, eq, elim)
#     return isolate_variable(tmp, want)





# def solve_system_alt(equations, values, want):

#     knowns = list(values.keys())

#     def check(eq, want):
#         eq_has_want = want in eq.free_symbols

#         eq_can_solve = eq.free_symbols.difference(knowns).difference({want}) == set()

#         return eq_has_want and eq_can_solve
    
#     tmp = next((eq for eq in equations if check(eq, want)), None)

#     if tmp is not None:
#         tmp = solve_system([tmp], values, want=want)
#         return tmp
        
#     tmp = equations[0]
#     for eq in equations[1:]:
#         elim_candidates = tmp.free_symbols.intersection(eq.free_symbols)
#         elim_candidates = elim_candidates.difference(knowns).difference({want})
#         if not elim_candidates:
#             raise ValueError("No suitable variable to eliminate found.")
#         elim = elim_candidates.pop()
#         tmp = combine_equations_sp(tmp, eq, elim)
#     return isolate_variable(tmp, want)



import sympy as sp

def _safe_simplify(expr):
    try:
        return sp.simplify(expr)
    except Exception:
        return expr

def _is_false_expr(expr):
    return expr is False or expr == sp.S.false

def _is_true_expr(expr):
    return expr is True or expr == sp.S.true

def filter_equations_for_unknowns(equations, unknowns, equations_sub=None):
    if equations_sub is None:
        equations_sub = equations
    if len(equations_sub) != len(equations):
        raise ValueError("equations_sub must be the same length as equations.")

    filtered = []
    for eq, eq_sub in zip(equations, equations_sub):
        if _is_true_expr(eq_sub):
            continue
        if _is_false_expr(eq_sub):
            raise ValueError("Inconsistent equation: False.")

        eq_sub_symbols = getattr(eq_sub, "free_symbols", set())
        if eq_sub_symbols & unknowns:
            filtered.append(eq)
            continue

        if isinstance(eq_sub, sp.Equality):
            diff = _safe_simplify(eq_sub.lhs - eq_sub.rhs)
            if getattr(diff, "free_symbols", set()):
                continue
            if _safe_simplify(diff) == 0:
                continue
            raise ValueError("Inconsistent equation with no unknowns.")

        simplified = _safe_simplify(eq_sub)
        if getattr(simplified, "free_symbols", set()):
            continue
        if simplified == 0 or _is_true_expr(simplified):
            continue
        if _is_false_expr(simplified):
            raise ValueError("Inconsistent equation with no unknowns.")
        raise ValueError("Inconsistent equation with no unknowns.")

    return filtered

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


# def solve_system_2(equations, values, want):

#     unknowns = connected_unknowns(equations, values, want)

#     unknowns = list(unknowns)

#     print("Solving for unknowns:", unknowns)

#     result = sp.solve(equations, unknowns, dict=True)

#     # from pprint import pprint
#     # pprint(result, sort_dicts=False)
    
#     return sp.Eq(want, result[0][want])

# def solve_system_multiple_solutions(equations, values, want):

#     unknowns = connected_unknowns(equations, values, want)

#     unknowns = list(unknowns)

#     print("Solving for unknowns:", unknowns)

#     solutions = sp.solve(equations, unknowns, dict=True)

#     if len(solutions) == 0:
#         raise ValueError("No solutions found.")
   
#     # print("Raw solutions:", solutions)

#     results = []
    
#     for item in solutions:
#         results.append(sp.Eq(want, item[want]))
    
#     return results




def clear_zero_denominators(eqs):
    out = []
    for eq in eqs:
        if not isinstance(eq, sp.Equality):
            out.append(eq)
            continue

        # Only do this for Eq(expr, 0) or Eq(0, expr)
        lhs, rhs = eq.lhs, eq.rhs
        if sp.simplify(rhs) == 0:
            expr = sp.together(lhs)
            num, den = sp.fraction(expr)
            out.append(sp.Eq(sp.simplify(num), 0))
        elif sp.simplify(lhs) == 0:
            expr = sp.together(rhs)
            num, den = sp.fraction(expr)
            out.append(sp.Eq(sp.simplify(num), 0))
        else:
            out.append(eq)

    return out



def solve_system_multiple_solutions(equations, values, want, check_knowns=False):

    unknowns = connected_unknowns(equations, values, want)

    unknowns = list(unknowns)

    print("Solving for unknowns:", unknowns)

    equations = clear_zero_denominators(equations)
    equations_sub = None
    if check_knowns:
        equations_sub = [eq.subs(values) for eq in equations]
    equations = filter_equations_for_unknowns(equations, set(unknowns), equations_sub)

    solutions = sp.solve(equations, unknowns, dict=True)

    if len(solutions) == 0:
        raise ValueError("No solutions found.")
   
    # print("Raw solutions:", solutions)

    results = []
    
    for item in solutions:
        results.append(sp.Eq(want, item[want]))
    
    return results
