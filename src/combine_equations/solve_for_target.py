# import sympy as sp

# def _simplify_expr(expr):
#     # A decent “pretty good” simplification pipeline.
#     # You can tweak this depending on your taste.
#     expr = sp.together(expr)
#     expr = sp.cancel(expr)
#     expr = sp.simplify(expr)
#     return expr

# def solve_for_target(
#     eqs,
#     target,
#     known=None,
#     exclude=None,
#     prefer_real=True,
#     allow_piecewise=False,
# ):
#     """
#     Solve eqs for `target`, optionally substituting known values first,
#     and optionally eliminating `exclude` symbols from the final expression.

#     Parameters
#     ----------
#     eqs : list[sp.Eq]
#         Equations defining the model.
#     target : sp.Symbol
#         The symbol to solve for.
#     known : dict[sp.Symbol, number/expr] | None
#         Known values to substitute early.
#     exclude : set[sp.Symbol] | list[sp.Symbol] | None
#         Symbols to eliminate (e.g., time t).
#     prefer_real : bool
#         If True, lightly prefer solutions without explicit I or complex branches.
#     allow_piecewise : bool
#         If False, reject Piecewise solutions when possible.

#     Returns
#     -------
#     sp.Expr
#         A closed-form expression for `target` if found.

#     Raises
#     ------
#     ValueError if no acceptable expression is found.
#     """

#     known = known or {}
#     exclude = set(exclude or [])

#     # 1) Substitute known values right away to reduce the system.
#     eqs_sub = [sp.Eq(_simplify_expr(e.lhs.subs(known)), _simplify_expr(e.rhs.subs(known))) for e in eqs]

#     # Collect symbols present after substitution
#     symset = set()
#     for e in eqs_sub:
#         symset |= e.free_symbols

#     # If target is already known, return it.
#     if target in known:
#         return sp.sympify(known[target])

#     # If target isn't in the system, nothing to do.
#     if target not in symset:
#         raise ValueError(f"Target {target} does not appear in the equations after substitution.")

#     # Candidates we can try to eliminate / solve over
#     # Unknowns are the remaining symbols minus anything known numeric-subbed out.
#     unknowns = list(symset - set(known.keys()))

#     # 2) Strategy A: direct solve for target from the whole system (best case)
#     candidates = []
#     try:
#         sol = sp.solve(eqs_sub, target, dict=True)
#         for s in sol:
#             if target in s:
#                 candidates.append(s[target])
#     except Exception:
#         pass

#     # 3) Strategy B: solve system for a set of unknowns including target
#     # (useful when direct solve doesn't trigger)
#     if not candidates:
#         try:
#             # Solve for all unknowns (or as many as possible)
#             sol = sp.solve(eqs_sub, unknowns, dict=True)
#             for s in sol:
#                 if target in s:
#                     candidates.append(s[target])
#         except Exception:
#             pass

#     # 4) Strategy C: eliminate excluded vars, then solve
#     # This is the closest to “auto elimination”.
#     if exclude:
#         try:
#             # sympy.eliminate expects expressions == 0 typically.
#             polys = [sp.expand(e.lhs - e.rhs) for e in eqs_sub]
#             eliminated = sp.eliminate(polys, *exclude)
#             # eliminated can be a single expression or a list
#             if isinstance(eliminated, (list, tuple, sp.Tuple)):
#                 elim_eqs = [sp.Eq(expr, 0) for expr in eliminated]
#             else:
#                 elim_eqs = [sp.Eq(eliminated, 0)]

#             # Now solve the eliminated constraints for the target
#             sol = sp.solve(elim_eqs, target, dict=True)
#             for s in sol:
#                 if target in s:
#                     candidates.append(s[target])
#         except Exception:
#             pass

#     # 5) Clean up, filter, rank
#     cleaned = []
#     for c in candidates:
#         c = _simplify_expr(c)
#         if not allow_piecewise and isinstance(c, sp.Piecewise):
#             continue
#         cleaned.append(c)

#     if not cleaned:
#         raise ValueError("No acceptable closed-form expression found for target.")

#     # Filter out expressions that still contain excluded symbols (if any)
#     if exclude:
#         cleaned_no_excl = [c for c in cleaned if not (c.free_symbols & exclude)]
#         if cleaned_no_excl:
#             cleaned = cleaned_no_excl

#     # Prefer “simpler” expressions
#     def score(expr):
#         s = sp.count_ops(expr)
#         # Light penalty if complex unit appears
#         if prefer_real and expr.has(sp.I):
#             s += 10_000
#         return s

#     cleaned.sort(key=score)
#     return cleaned[0]


# https://chatgpt.com/c/695400c2-13dc-8331-89b9-0b8ce176fdbb

import sympy as sp

def solve_for_target(
    eqs,
    target,
    known=None,
    exclude=None,
):
    known = known or {}
    exclude = set(exclude or [])

    # Substitute knowns early
    eqs_sub = [sp.Eq(e.lhs.subs(known), e.rhs.subs(known)) for e in eqs]

    # Unknown symbols still present
    symset = set().union(*(e.free_symbols for e in eqs_sub))
    unknowns = list(symset - set(known.keys()))

    # If we want to eliminate exclude vars, ask solve() to do it
    if exclude:
        sol = sp.solve(
            eqs_sub,
            target,
            dict=True,
            eliminate=True,            # <- key
            exclude=list(exclude),     # <- key
        )
    else:
        sol = sp.solve(eqs_sub, target, dict=True)

    if not sol:
        raise ValueError("No solution found.")

    # Pick the “simplest” candidate
    candidates = [s[target] for s in sol if target in s]
    if not candidates:
        raise ValueError("Target not solved for.")

    candidates = [sp.simplify(sp.cancel(sp.together(c))) for c in candidates]
    candidates.sort(key=sp.count_ops)
    return candidates[0]
