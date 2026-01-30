"""
Simple demo of the equation GUI with a basic kinematics problem.
"""

import sys
sys.path.insert(0, 'src')

from combine_equations.equation_gui import show_equation_gui
from combine_equations.kinematics_states import make_states_model, kinematics_fundamental
from sympy.physics.units import m, s

# Create a simple kinematics problem
b = make_states_model("b", 2)  # baseball
b0, b1 = b.states
b01 = b.edges[0]

# Generate kinematic equations
eqs = kinematics_fundamental(b, axes=['x'])

# Known values
values = {}
values[b0.pos.x] = 0 * m
values[b1.pos.x] = 1.50 * m
values[b0.vel.x] = 0 * m/s
values[b1.vel.x] = 45.0 * m/s
values[b0.t] = 0 * s

# Target: find acceleration
want = b01.a.x

# Launch GUI
print("Launching Equation GUI...")
print("\nFeatures:")
print("  - Click on any symbol to highlight all occurrences")
print("  - Right-click on a symbol to eliminate it from equations")
print("  - History shows all operations performed")
print("\nTry right-clicking on 'v_av_x_b_0_1' to eliminate it!")

show_equation_gui(eqs, values, want, "Fast Pitch Problem")
