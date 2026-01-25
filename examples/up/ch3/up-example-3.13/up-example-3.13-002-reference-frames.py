# You drive north on a straight two-lane road at a constant 88 km/h.
# 
# A truck in the other lane approaches you at a constant 104 km/h (Fig. 3.33).
# 
# Find 
# 
# (a) the truck's velocity relative to you and 
# 
# (b) your velocity relative to the truck.
# 
# (c) How do the relative velocities change after you and the
# truck pass each other?
# 
# Treat this as a one-dimensional problem.

from sympy.physics.vector import ReferenceFrame, Point
from sympy.physics.vector import init_vprinting
import sympy as sp

init_vprinting(pretty_print=False)

# ==============================================================================
# Define Reference Frames
# ==============================================================================

# Earth frame (inertial reference frame)
E = ReferenceFrame('E')

# Your reference frame (moving relative to Earth)
Y = ReferenceFrame('Y')

# Truck's reference frame (moving relative to Earth)
T = ReferenceFrame('T')

# ==============================================================================
# Define Points
# ==============================================================================

# We'll define points to track positions, though for this problem
# we only care about velocities

# Origin point on Earth (stationary)
O = Point('O')
O.set_vel(E, 0)

# Point representing You
P_Y = Point('P_Y')

# Point representing Truck
P_T = Point('P_T')

# ==============================================================================
# Set velocities relative to Earth
# ==============================================================================

# Your velocity: 88 km/h north (positive x direction)
v_YE_value = 88  # km/h
P_Y.set_vel(E, v_YE_value * E.x)

# Truck's velocity: 104 km/h south (negative x direction, approaching)
v_TE_value = -104  # km/h (negative because moving south)
P_T.set_vel(E, v_TE_value * E.x)

print("=" * 80)
print("Velocities relative to Earth (E):")
print("=" * 80)
print(f"Your velocity relative to Earth:   P_Y.vel(E) = {P_Y.vel(E)}")
print(f"Truck velocity relative to Earth:  P_T.vel(E) = {P_T.vel(E)}")
print()

# ==============================================================================
# Calculate relative velocities
# ==============================================================================

# (a) Truck's velocity relative to You
# We need to express the truck's velocity in your reference frame

# Set the angular velocity between frames (0 since no rotation)
Y.set_ang_vel(E, 0)
T.set_ang_vel(E, 0)

# Position vectors (we can set these arbitrarily since we only care about velocity)
P_Y.set_pos(O, 0)
P_T.set_pos(O, 0)

# Calculate relative velocity: v_T/Y = v_T/E - v_Y/E
v_TY = P_T.vel(E) - P_Y.vel(E)

print("=" * 80)
print("(a) Truck's velocity relative to You:")
print("=" * 80)
print(f"v_T/Y = v_T/E - v_Y/E")
print(f"v_T/Y = {P_T.vel(E)} - ({P_Y.vel(E)})")
print(f"v_T/Y = {v_TY}")
print()
print(f"Magnitude: {v_TY.magnitude()} km/h")
print("Interpretation: The truck is approaching you at 192 km/h")
print()

# ==============================================================================
# (b) Your velocity relative to Truck
# ==============================================================================

# Calculate relative velocity: v_Y/T = v_Y/E - v_T/E
v_YT = P_Y.vel(E) - P_T.vel(E)

print("=" * 80)
print("(b) Your velocity relative to Truck:")
print("=" * 80)
print(f"v_Y/T = v_Y/E - v_T/E")
print(f"v_Y/T = {P_Y.vel(E)} - ({P_T.vel(E)})")
print(f"v_Y/T = {v_YT}")
print()
print(f"Magnitude: {v_YT.magnitude()} km/h")
print("Interpretation: You are approaching the truck at 192 km/h (positive direction)")
print()

# ==============================================================================
# (c) After passing each other
# ==============================================================================

print("=" * 80)
print("(c) After you and the truck pass each other:")
print("=" * 80)
print("The relative velocities do NOT change!")
print()
print("Even though the relative POSITIONS change (truck is now behind you),")
print("the relative VELOCITIES remain the same because both vehicles continue")
print("at constant speeds in opposite directions.")
print()
print(f"v_T/Y still = {v_TY}")
print(f"v_Y/T still = {v_YT}")
print()

# ==============================================================================
# Verification using the velocity transformation equation
# ==============================================================================

print("=" * 80)
print("VERIFICATION: Relative Velocity Equations")
print("=" * 80)
print()
print("The general equation for relative velocity is:")
print("  v_A/B = v_A/C - v_B/C")
print()
print("This is equivalent to:")
print("  v_A/C = v_A/B + v_B/C")
print()
print("Checking our values:")
v_TE_check = v_TY + P_Y.vel(E)
print(f"  v_T/E = v_T/Y + v_Y/E")
print(f"  {P_T.vel(E)} = {v_TY} + {P_Y.vel(E)}")
print(f"  {P_T.vel(E)} = {v_TE_check}")
print(f"  ✓ Verified!")
print()

# Check the relationship v_Y/T = -v_T/Y
print("Also note that:")
print(f"  v_Y/T = -v_T/Y")
print(f"  {v_YT} = -({v_TY})")
print(f"  {v_YT} = {-v_TY}")
print(f"  ✓ Verified!")
print()
