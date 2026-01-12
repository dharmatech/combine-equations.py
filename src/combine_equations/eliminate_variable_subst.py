import sympy as sp


def _safe_simplify(expr):
    try:
        return sp.simplify(expr)
    except Exception:
        return expr

def _is_tautology(eq):
    # Covers Python bool, SymPy BooleanTrue, and Eq(x, x)
    if eq is True or eq == sp.S.true:
        return True
    if isinstance(eq, sp.Equality):
        # If lhs-rhs simplifies to 0, it's tautological
        return _safe_simplify(eq.lhs - eq.rhs) == 0
    return False

def cleanup_equations(eqs):
    out = []
    for e in eqs:
        if _is_tautology(e):
            continue
        out.append(e)
    return out


# def eliminate_variable_subst(equations, var, max_passes=10):
#     """
#     Eliminate `var` from a list of Eq's by substitution whenever possible.

#     It looks for equations that can be solved for `var` (including var=expr and expr=var),
#     builds a replacement var -> expr, substitutes into all equations, and drops tautologies.

#     Returns: (new_equations, replacement_expr_or_None)
#     """
#     eqs = list(equations)
#     replacement = None

#     for _ in range(max_passes):
#         # 1) find candidate expressions for var from any single equation
#         candidates = []
#         for eq in eqs:
#             if not isinstance(eq, sp.Equality):
#                 continue
#             if var not in eq.free_symbols:
#                 continue
#             try:
#                 sols = sp.solve(eq, var)  # returns list of expressions
#             except Exception:
#                 continue
#             for s in sols:
#                 # avoid self-referential replacements like var -> var + 1
#                 if var in sp.sympify(s).free_symbols:
#                     continue
#                 candidates.append(sp.simplify(s))

#         if not candidates:
#             break

#         # 2) pick "best" candidate (simplest)
#         candidates.sort(key=sp.count_ops)
#         replacement = candidates[0]

#         # 3) substitute into all equations and simplify
#         new_eqs = []
#         for eq in eqs:
#             new_eq = eq.subs({var: replacement})
#             # SymPy can reduce Eq to True/False after subs
#             if new_eq is True:
#                 continue
#             if new_eq is False:
#                 # keep False to indicate inconsistency
#                 new_eqs.append(new_eq)
#                 continue
#             new_eqs.append(sp.simplify(new_eq))

#         eqs = new_eqs

#         # stop if var is gone everywhere
#         if all((not isinstance(e, sp.Equality)) or (var not in e.free_symbols) for e in eqs):
#             break

#     return eqs, replacement

# equations = tmp
# var = b1.vel.x
# eq = eqs[0]

# s = sols[0]

def eliminate_variable_subst(equations, var, max_passes=10):
    eqs = list(equations)
    replacement = None

    for _ in range(max_passes):
        candidates = []
        for eq in eqs:
            if not isinstance(eq, sp.Equality):
                continue
            if var not in eq.free_symbols:
                continue
            try:
                sols = sp.solve(eq, var)

                if len(sols) == 0:
                    print("Warning: No solutions found when solving for variable.")
                    print(f"Equation: {eq}, Variable: {var}")
            except Exception:
                continue
            for s in sols:
                s = sp.sympify(s)
                if var in s.free_symbols:
                    continue
                candidates.append(_safe_simplify(s))

        if not candidates:
            break

        candidates.sort(key=sp.count_ops)
        replacement = candidates[0]


        # https://github.com/sympy/sympy/issues/28926
        # Once this is fixed, try regular sp.simplify again
        # instead of _safe_simplify
        eqs = [_safe_simplify(e.subs({var: replacement})) for e in eqs]
        eqs = cleanup_equations(eqs)

        if all((not isinstance(e, sp.Equality)) or (var not in e.free_symbols) for e in eqs):
            break

    return eqs, replacement
