
import sympy as sp

def display_equation(eq):
    # sp.pprint(eq)
    # print(f"{eq_2.lhs} = {eq_2.rhs}")
    print(f'{eq.lhs} = {eq.rhs}')

def symbols_in_common_sp(eq1, eq2):
    return eq1.free_symbols.intersection(eq2.free_symbols)

# def symbols_in_common(eq1, eq2):
#     return eq1.symbol_set.intersection(eq2.symbol_set)


def isolate_variable(equation, variable):
    solution = sp.solve(equation, variable)
    if solution:
        return sp.Eq(variable, solution[0])
    else:
        raise ValueError(f"Could not isolate variable {variable} in the given equation.")

def combine_equations_sp(eq1, eq2, elim):
    common = symbols_in_common_sp(eq1, eq2)
    if elim not in common:
        raise ValueError('elim must be one of the common symbols')
    
    isolated = isolate_variable(eq2, elim)
    
    substituted = eq1.subs(elim, isolated.rhs)

    return substituted

def format_equation(eq, padding=0):
    if padding > 0:
        return f'{str(eq.lhs):<{padding}} = {eq.rhs}'
    else:
        return f'{eq.lhs} = {eq.rhs}'


def multiply_both_sides(eq, factor):
    return sp.Eq(eq.lhs * factor, eq.rhs * factor)

def divide_both_sides(eq, divisor):
    return sp.Eq(eq.lhs / divisor, eq.rhs / divisor)

def expand_lhs(eq):
    return sp.Eq(sp.expand(eq.lhs), eq.rhs)

def expand_rhs(eq):
    return sp.Eq(eq.lhs, sp.expand(eq.rhs))

def matches_existing(equation, equation_table):
    for eq in equation_table.values():
        if equation.free_symbols == eq.free_symbols:
            display_equation(eq)
            return True
    return False

def add_if_new(label, equation, equation_table):
    for eq in equation_table.values():
        if equation.free_symbols == eq.free_symbols:
            return False
    equation_table[label] = equation
    return True




