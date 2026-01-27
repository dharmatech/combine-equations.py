
import sympy as sp
from combine_equations.display_equations import display_equation_

# ----------------------------------------------------------------------
def solve_subs(eq_a, eq_b, var):

    result = sp.solve(eq_b, var)

    if len(result) == 1:
        return eq_a.subs(var, result[0])

    raise ValueError("Multiple solutions found; cannot substitute uniquely.")

def symbols_in_common(eq_a, eq_b):
    return eq_a.free_symbols.intersection(eq_b.free_symbols)
# ----------------------------------------------------------------------

class EquationWithHistory:
    """
    Represents an equation with metadata about its derivation history.
    
    This allows intelligent combination of equations by preventing:
    - Combining an equation with its parents (circular logic)
    - Combining an equation with its children (redundant)
    - Combining siblings (same parents)
    """
    
    _next_id = 0
    
    def __init__(self, equation, parents=None, eliminated_symbol=None, name=None):
        self.eq = sp.simplify(equation)
        self.parents = frozenset(parents) if parents else frozenset()
        self.eliminated_symbol = eliminated_symbol
        self.is_fundamental = len(self.parents) == 0
        self.name = name
        
        # Assign unique ID for tracking
        self.id = EquationWithHistory._next_id
        EquationWithHistory._next_id += 1
        
        # Compute all ancestors (parents + their ancestors recursively)
        self.ancestors = self._compute_ancestors()
    
    def _compute_ancestors(self):
        """Recursively compute all ancestors (parents, grandparents, etc.)."""
        if not self.parents:
            return frozenset()
        
        ancestors = set(self.parents)
        for parent in self.parents:
            ancestors.update(parent.ancestors)
        
        return frozenset(ancestors)
        
    def can_combine_with(self, other):
        """
        Determine if this equation can be meaningfully combined with another.
        
        Returns False if:
        - other is an ancestor of this equation
        - this is an ancestor of other
        - both have the same parents (siblings)
        - they share any common ancestors (would reuse same information)
        """
        if not isinstance(other, EquationWithHistory):
            return False
            
        # Don't combine with any ancestor
        if other in self.ancestors:
            return False
            
        # Don't combine with any descendant (this is ancestor of other)
        if self in other.ancestors:
            return False
            
        # Don't combine with a sibling (same parents)
        if self.parents and other.parents and self.parents == other.parents:
            return False
        
        # Don't combine if they share any common ancestors
        # This prevents using the same fundamental equation's information multiple times
        if self.ancestors and other.ancestors:
            common_ancestors = self.ancestors.intersection(other.ancestors)
            if common_ancestors:
                return False
            
        return True
    
    def derive_from(self, other_eq, symbol):
        """
        Create a new equation by solving other_eq for symbol and substituting into self.
        
        Args:
            other_eq: Another EquationWithHistory object
            symbol: The symbol to eliminate
            
        Returns:
            A new EquationWithHistory with both self and other_eq as parents
        """
        new_eq = solve_subs(self.eq, other_eq.eq, symbol)
        
        return EquationWithHistory(
            new_eq,
            parents={self, other_eq},
            eliminated_symbol=symbol
        )
    
    def get_history(self, show_parent_history=False):
        """Get a concise description of how this equation was derived.
        
        Args:
            show_parent_history: If True, show the derivation of non-fundamental parents
        """
        if self.is_fundamental:
            return self.name or f"#{self.id}"
        
        # Show immediate parents
        parent_list = sorted(self.parents, key=lambda p: p.id)
        
        if show_parent_history:
            parent_strs = []
            for p in parent_list:
                if p.is_fundamental:
                    parent_strs.append(p.name or f"#{p.id}")
                else:
                    # Show derived parents with their history in brackets
                    parent_strs.append(f"[{p.get_history()}]")
        else:
            parent_strs = [p.name or f"#{p.id}" for p in parent_list]
        
        return f"{' + '.join(parent_strs)} (eliminate {self.eliminated_symbol})"
    
    def get_full_history(self, indent=0):
        """Get a full recursive history showing all derivation steps."""
        prefix = "  " * indent
        
        if self.is_fundamental:
            return f"{prefix}{self.name or f'#{self.id}'} (FUNDAMENTAL)"
        
        lines = [f"{prefix}{self.name or f'#{self.id}'} = {self.get_history()}"]
        
        # Recursively show parent histories
        for parent in sorted(self.parents, key=lambda p: p.id):
            if not parent.is_fundamental:
                lines.append(parent.get_full_history(indent + 1))
        
        return "\n".join(lines)
    
    def __repr__(self):
        return f"<Eq {self.get_history()}>"
    
    def __hash__(self):
        return self.id
    
    def __eq__(self, other):
        if not isinstance(other, EquationWithHistory):
            return False
        return self.id == other.id


def is_algebraically_equivalent(eq1, eq2):
    """Check if two equations are algebraically equivalent."""
    try:
        diff = sp.simplify(eq1.lhs - eq1.rhs - (eq2.lhs - eq2.rhs))
        return diff == 0
    except:
        return False


def is_duplicate(new_eq_obj, existing_equations):
    """Check if new equation is algebraically equivalent to any existing equation."""
    for existing in existing_equations:
        if is_algebraically_equivalent(new_eq_obj.eq, existing.eq):
            return True
    return False


def derive_all_equations(fundamental_equations, max_depth=3, verbose=True):
    """
    Systematically derive all possible equations from fundamental equations.
    
    Args:
        fundamental_equations: List of (equation, name) tuples or just equations
        max_depth: Maximum number of substitution rounds
        verbose: Print progress information
        
    Returns:
        Set of all EquationWithHistory objects (fundamental + derived)
    """
    # Wrap fundamental equations
    eq_objs = []
    for item in fundamental_equations:
        if isinstance(item, tuple):
            eq, name = item
            eq_objs.append(EquationWithHistory(eq, name=name))
        else:
            eq_objs.append(EquationWithHistory(item))
    
    all_equations = set(eq_objs)
    
    if verbose:
        print(f"Starting with {len(eq_objs)} fundamental equations\n")
    
    for depth in range(max_depth):
        new_round = []
        attempts = 0
        skipped = 0
        
        for eq_a in all_equations:
            for eq_b in all_equations:
                if eq_a == eq_b:
                    continue
                
                # Only try one ordering to avoid symmetric duplicates
                # solve_subs(eq_a, eq_b, x) and solve_subs(eq_b, eq_a, x) are typically equivalent
                if eq_a.id > eq_b.id:
                    continue
                    
                if not eq_a.can_combine_with(eq_b):
                    skipped += 1
                    continue
                
                common = symbols_in_common(eq_a.eq, eq_b.eq)
                
                for symbol in common:
                    attempts += 1
                    try:
                        new_eq_obj = eq_a.derive_from(eq_b, symbol)
                        
                        if not is_duplicate(new_eq_obj, all_equations):
                            new_round.append(new_eq_obj)
                            if verbose:
                                print(f"  Derived: {new_eq_obj.get_history(show_parent_history=True)}")
                                display_equation_(new_eq_obj.eq)
                                print()
                    except Exception as e:
                        # Some substitutions may fail (multiple solutions, etc.)
                        pass
        
        if verbose:
            print(f"Depth {depth + 1}: Tried {attempts} combinations, skipped {skipped}, found {len(new_round)} new equations\n")
        
        if not new_round:
            if verbose:
                print("No new equations found. Stopping.\n")
            break
        
        all_equations.update(new_round)
    
    if verbose:
        print(f"Total equations: {len(all_equations)} ({len(eq_objs)} fundamental + {len(all_equations) - len(eq_objs)} derived)")
    
    return all_equations

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
eq_2_2 = sp.Eq(v_av_x, (x_2 - x_1) / dt)

eq_2_7 = sp.Eq(a_x, (v_2x - v_1x) / dt)

eq_2_10 = sp.Eq(v_av_x, (v_1x + v_2x) / 2)
# ----------------------------------------------------------------------
# Example usage
# ----------------------------------------------------------------------

fundamental = [
    (eq_2_2, "eq_2.2"),
    (eq_2_7, "eq_2.7"),
    (eq_2_10, "eq_2.10")
]

all_eqs = derive_all_equations(fundamental, max_depth=3, verbose=True)

print("\n" + "="*60)
print("ALL DERIVED EQUATIONS:")
print("="*60)

# Sort: fundamental first, then by ID
sorted_eqs = sorted(all_eqs, key=lambda e: (not e.is_fundamental, e.id))

for eq_obj in sorted_eqs:
    if eq_obj.is_fundamental:
        print(f"\n{eq_obj.name} (FUNDAMENTAL):")
    else:
        print(f"\n{eq_obj.get_history()}:")
    display_equation_(eq_obj.eq)

print("\n" + "="*60)
print("FULL DERIVATION TREE:")
print("="*60)

# Show full history for non-fundamental equations
for eq_obj in sorted_eqs:
    if not eq_obj.is_fundamental:
        print(f"\n{eq_obj.get_full_history()}")

# ----------------------------------------------------------------------

# > python .\archive\kinematic-equations\kinematics-equations-005-eq-history.py
# Starting with 3 fundamental equations
# 
#   Derived: eq_2.2 + eq_2.7 (eliminate dt)
# v_av_x = a_x*(x_1 - x_2)/(v_1x - v_2x)
# 
#   Derived: eq_2.2 + eq_2.10 (eliminate v_av_x)
# v_1x/2 + v_2x/2 = (-x_1 + x_2)/dt
# 
#   Derived: eq_2.7 + eq_2.10 (eliminate v_1x)
# a_x = 2*(v_2x - v_av_x)/dt
# 
#   Derived: eq_2.7 + eq_2.10 (eliminate v_2x)
# a_x = 2*(-v_1x + v_av_x)/dt
# 
# Depth 1: Tried 4 combinations, skipped 0, found 4 new equations
# 
#   Derived: eq_2.2 + [eq_2.7 + eq_2.10 (eliminate v_1x)] (eliminate v_av_x)
# a_x*dt/2 - v_2x = -(-x_1 + x_2)/dt
# 
#   Derived: eq_2.2 + [eq_2.7 + eq_2.10 (eliminate v_1x)] (eliminate dt)
# v_av_x = a_x*(-x_1 + x_2)/(2*(v_2x - v_av_x))
# 
#   Derived: eq_2.2 + [eq_2.7 + eq_2.10 (eliminate v_2x)] (eliminate v_av_x)
# a_x*dt/2 + v_1x = (-x_1 + x_2)/dt
# 
#   Derived: eq_2.2 + [eq_2.7 + eq_2.10 (eliminate v_2x)] (eliminate dt)
# v_av_x = a_x*(x_1 - x_2)/(2*(v_1x - v_av_x))
# 
#   Derived: eq_2.7 + [eq_2.2 + eq_2.10 (eliminate v_av_x)] (eliminate v_1x)
# a_x = 2*(dt*v_2x + x_1 - x_2)/dt**2
# 
#   Derived: eq_2.7 + [eq_2.2 + eq_2.10 (eliminate v_av_x)] (eliminate v_2x)
# a_x = 2*(-dt*v_1x - x_1 + x_2)/dt**2
# 
#   Derived: eq_2.7 + [eq_2.2 + eq_2.10 (eliminate v_av_x)] (eliminate dt)
# a_x = (v_1x - v_2x)*(v_1x + v_2x)/(2*(x_1 - x_2))
# 
#   Derived: eq_2.10 + [eq_2.2 + eq_2.7 (eliminate dt)] (eliminate v_1x)
# v_2x - 2*v_av_x = -(a_x*x_1 - a_x*x_2 + v_2x*v_av_x)/v_av_x
# 
#   Derived: eq_2.10 + [eq_2.2 + eq_2.7 (eliminate dt)] (eliminate v_2x)
# v_1x = a_x*x_1/v_av_x - a_x*x_2/v_av_x - v_1x + 2*v_av_x
# 
#   Derived: eq_2.10 + [eq_2.2 + eq_2.7 (eliminate dt)] (eliminate v_av_x)
# v_1x = (2*a_x*(x_1 - x_2) - v_2x*(v_1x - v_2x))/(v_1x - v_2x)
# 
# Depth 2: Tried 14 combinations, skipped 14, found 10 new equations
# 
# Depth 3: Tried 14 combinations, skipped 129, found 0 new equations
# 
# No new equations found. Stopping.
# 
# Total equations: 17 (3 fundamental + 14 derived)
# 
# ============================================================
# ALL DERIVED EQUATIONS:
# ============================================================
# 
# eq_2.2 (FUNDAMENTAL):
# v_av_x = (-x_1 + x_2)/dt
# 
# eq_2.7 (FUNDAMENTAL):
# a_x = (-v_1x + v_2x)/dt
# 
# eq_2.10 (FUNDAMENTAL):
# v_1x = -v_2x + 2*v_av_x
# 
# eq_2.2 + eq_2.7 (eliminate dt):
# v_av_x = a_x*(x_1 - x_2)/(v_1x - v_2x)
# 
# eq_2.2 + eq_2.10 (eliminate v_av_x):
# v_1x/2 + v_2x/2 = (-x_1 + x_2)/dt
# 
# eq_2.7 + eq_2.10 (eliminate v_1x):
# a_x = 2*(v_2x - v_av_x)/dt
# 
# eq_2.7 + eq_2.10 (eliminate v_2x):
# a_x = 2*(-v_1x + v_av_x)/dt
# 
# eq_2.2 + #5 (eliminate v_av_x):
# a_x*dt/2 - v_2x = -(-x_1 + x_2)/dt
# 
# eq_2.2 + #5 (eliminate dt):
# v_av_x = a_x*(-x_1 + x_2)/(2*(v_2x - v_av_x))
# 
# eq_2.2 + #6 (eliminate v_av_x):
# a_x*dt/2 + v_1x = (-x_1 + x_2)/dt
# 
# eq_2.2 + #6 (eliminate dt):
# v_av_x = a_x*(x_1 - x_2)/(2*(v_1x - v_av_x))
# 
# eq_2.7 + #4 (eliminate v_1x):
# a_x = 2*(dt*v_2x + x_1 - x_2)/dt**2
# 
# eq_2.7 + #4 (eliminate v_2x):
# a_x = 2*(-dt*v_1x - x_1 + x_2)/dt**2
# 
# eq_2.7 + #4 (eliminate dt):
# a_x = (v_1x - v_2x)*(v_1x + v_2x)/(2*(x_1 - x_2))
# 
# eq_2.10 + #3 (eliminate v_1x):
# v_2x - 2*v_av_x = -(a_x*x_1 - a_x*x_2 + v_2x*v_av_x)/v_av_x
# 
# eq_2.10 + #3 (eliminate v_2x):
# v_1x = a_x*x_1/v_av_x - a_x*x_2/v_av_x - v_1x + 2*v_av_x
# 
# eq_2.10 + #3 (eliminate v_av_x):
# v_1x = (2*a_x*(x_1 - x_2) - v_2x*(v_1x - v_2x))/(v_1x - v_2x)
# 
# ============================================================
# FULL DERIVATION TREE:
# ============================================================
# 
# #3 = eq_2.2 + eq_2.7 (eliminate dt)
# 
# #4 = eq_2.2 + eq_2.10 (eliminate v_av_x)
# 
# #5 = eq_2.7 + eq_2.10 (eliminate v_1x)
# 
# #6 = eq_2.7 + eq_2.10 (eliminate v_2x)
# 
# #9 = eq_2.2 + #5 (eliminate v_av_x)
#   #5 = eq_2.7 + eq_2.10 (eliminate v_1x)
# 
# #10 = eq_2.2 + #5 (eliminate dt)
#   #5 = eq_2.7 + eq_2.10 (eliminate v_1x)
# 
# #11 = eq_2.2 + #6 (eliminate v_av_x)
#   #6 = eq_2.7 + eq_2.10 (eliminate v_2x)
# 
# #12 = eq_2.2 + #6 (eliminate dt)
#   #6 = eq_2.7 + eq_2.10 (eliminate v_2x)
# 
# #15 = eq_2.7 + #4 (eliminate v_1x)
#   #4 = eq_2.2 + eq_2.10 (eliminate v_av_x)
# 
# #16 = eq_2.7 + #4 (eliminate v_2x)
#   #4 = eq_2.2 + eq_2.10 (eliminate v_av_x)
# 
# #17 = eq_2.7 + #4 (eliminate dt)
#   #4 = eq_2.2 + eq_2.10 (eliminate v_av_x)
# 
# #18 = eq_2.10 + #3 (eliminate v_1x)
#   #3 = eq_2.2 + eq_2.7 (eliminate dt)
# 
# #19 = eq_2.10 + #3 (eliminate v_2x)
#   #3 = eq_2.2 + eq_2.7 (eliminate dt)
# 
# #20 = eq_2.10 + #3 (eliminate v_av_x)
#   #3 = eq_2.2 + eq_2.7 (eliminate dt)