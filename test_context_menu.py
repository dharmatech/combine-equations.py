"""
Quick test to verify the context menu feature in Jupyter GUI.
Run this in a Jupyter notebook environment.
"""

from sympy import symbols, Eq
from combine_equations.equation_gui_jupyter import show_equation_gui_jupyter

# Simple system of equations
x, y, z = symbols('x y z')
equations = [
    Eq(x + y, 10),
    Eq(y + z, 15),
    Eq(x + z, 13)
]

# Known and target values
values = {x: 4}
want = z

print("Testing equation GUI with context menu feature")
print("=" * 50)
print()
print("Instructions:")
print("1. Left-click on any symbol to highlight it across all equations")
print("2. Right-click on any symbol to see context menu with options:")
print("   - Eliminate variable (auto)")
print("   - Eliminate using specific equation")
print("   - Clear selection")
print("3. You can also use the dropdown menus at the top")
print()
print("=" * 50)
print()

# Display the GUI
gui = show_equation_gui_jupyter(equations, values=values, want=want)
