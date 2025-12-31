
import sympy as sp

def display_equations(equations):
    for eq in equations:
        print(f'{eq.lhs} = {eq.rhs}')

# def display_equations_(equations, want):
#     for eq in equations:
#         print(f'{eq.lhs} = {eq.rhs}')

# def display_equation_(eq, want):
#     print(f'{eq.lhs} = {eq.rhs}')

def red_text(s):
    RED = "\x1b[31m"
    RESET = "\x1b[0m"
    return f"{RED}{s}{RESET}"

def green_text(s):
    GREEN = "\x1b[32m"
    RESET = "\x1b[0m"
    return f"{GREEN}{s}{RESET}"

# def display_equation_(eq, want):
#     colored_want = sp.Symbol(red_text(str(want)))
#     eq = eq.subs({want: colored_want})
#     print(f'{eq.lhs} = {eq.rhs}')

# def display_equation_(eq, values, want):

#     colored_want = sp.Symbol(red_text(str(want)))

#     eq = eq.subs({want: colored_want})
    
#     colored_knowns = {}

#     for sym in values.keys():
#         colored_knowns[sym] = sp.Symbol(green_text(str(sym)))

#     eq = eq.subs(colored_knowns)

#     print(f'{eq.lhs} = {eq.rhs}')

def display_equation_(eq, values=None, want=None):

    if want is not None:
        colored_want = sp.Symbol(red_text(str(want)))
        eq = eq.subs({want: colored_want})

    if values is not None:
        colored_knowns = {}

        for sym in values.keys():
            colored_knowns[sym] = sp.Symbol(green_text(str(sym)))

        eq = eq.subs(colored_knowns)

    print(f'{eq.lhs} = {eq.rhs}')

def display_equations_(equations, values=None, want=None):
    for eq in equations:
        display_equation_(eq, values, want)