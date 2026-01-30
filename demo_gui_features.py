"""
Comprehensive demo showing all GUI features.

This example demonstrates:
1. Color-coded equation display (green=known, red=target)
2. Click-to-highlight symbols
3. Right-click to eliminate variables
4. History/transaction tracking
"""

import sys
sys.path.insert(0, 'src')

from combine_equations.equation_gui import show_equation_gui
from combine_equations.kinematics_states import make_states_model, kinematics_fundamental
from sympy.physics.units import m, s

print("=" * 70)
print("EQUATION GUI DEMO - Fast Pitch Baseball Problem")
print("=" * 70)
print()
print("Problem:")
print("  A baseball leaves the pitcher's hand at 45.0 m/s")
print("  The ball was accelerated over a distance of 1.50 m")
print("  Find: (a) the acceleration, (b) the time")
print()
print("=" * 70)
print()

# Setup the physics model
b = make_states_model("b", 2)  # baseball with 2 states
b0, b1 = b.states  # initial and final states
b01 = b.edges[0]   # the interval between states

# Generate fundamental kinematic equations
eqs = kinematics_fundamental(b, axes=['x'])

# Define known values
values = {}
values[b0.pos.x] = 0 * m      # starts at origin
values[b1.pos.x] = 1.50 * m   # ends at 1.5 m
values[b0.vel.x] = 0 * m/s    # starts from rest
values[b1.vel.x] = 45.0 * m/s # final velocity
values[b0.t] = 0 * s          # time starts at 0

# Target variable (will be shown in RED)
want = b01.a.x  # we want to find acceleration

print("GUI FEATURES TO TRY:")
print("-" * 70)
print()
print("1. HIGHLIGHTING:")
print("   → Left-click any symbol to highlight all instances")
print("   → Try clicking 'b_0_v_x' or 'dt_b_0_1'")
print()
print("2. COLOR CODING:")
print("   → Green symbols = known values (from problem statement)")
print("   → Red symbol = target variable (what we're solving for)")
print("   → Black symbols = unknowns to be eliminated")
print()
print("3. VARIABLE ELIMINATION:")
print("   → Right-click on 'v_av_x_b_0_1' (average velocity)")
print("   → Select 'Eliminate' from the context menu")
print("   → Watch it disappear and equations simplify!")
print()
print("4. HISTORY TRACKING:")
print("   → Each operation adds a new entry to the history")
print("   → Scroll up to see previous states")
print("   → See exactly what was substituted")
print()
print("5. TRY THIS SEQUENCE:")
print("   a) Right-click 'v_av_x_b_0_1' → Eliminate")
print("   b) Right-click 'dt_b_0_1' → Eliminate")
print("   c) See how the equations simplify step by step!")
print()
print("=" * 70)
print()
print("Launching GUI...")

# Launch the interactive GUI
show_equation_gui(eqs, values, want, "Fast Pitch Problem - Find acceleration")
