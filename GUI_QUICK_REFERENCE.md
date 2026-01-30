# Equation GUI - Quick Reference

## Launch GUI

```python
from combine_equations.equation_gui import show_equation_gui

show_equation_gui(equations, values, want, description)
```

**Parameters:**
- `equations`: List of SymPy Eq objects
- `values`: Dict mapping symbols to their known values (displayed in **green**)
- `want`: Target symbol to solve for (displayed in **red**)
- `description`: String describing this step

## Mouse Interactions

| Action | Effect |
|--------|--------|
| **Left-click symbol** | Highlight all instances of that symbol (yellow background) |
| **Right-click symbol** | Open context menu with elimination option |
| **Mouse wheel** | Scroll through history |

## Context Menu Options

When you right-click a symbol:
- **Eliminate 'symbol'**: Remove that variable by substitution
- **Clear selection**: Unhighlight all symbols

## Color Coding

| Color | Meaning |
|-------|---------|
| 🟢 **Green** | Known values (in `values` dict) |
| 🔴 **Red** | Target variable (`want`) |
| ⚫ **Black** | Unknown variables |
| 🟡 **Yellow bg** | Selected/highlighted symbol |

## History View

The GUI shows a growing history of operations:

```
▶ Initial equations
  dt_b_0_1 = -b_0_t + b_1_t
  v_av_x_b_0_1 = (-b_0_x + b_1_x)/dt_b_0_1
  ...

────────────────────────────────────

▶ Eliminated v_av_x_b_0_1 → (-b_0_x + b_1_x)/dt_b_0_1
  dt_b_0_1 = -b_0_t + b_1_t
  a_x_b_0_1 = (-b_0_v_x + b_1_v_x)/dt_b_0_1
  ...

────────────────────────────────────

▶ Eliminated dt_b_0_1 → -b_0_t + b_1_t
  a_x_b_0_1 = (-b_0_v_x + b_1_v_x)/(-b_0_t + b_1_t)
  ...
```

## Tips

1. **Start by highlighting**: Click symbols to understand where they appear
2. **Eliminate strategically**: Right-click intermediate variables first
3. **Use the history**: Scroll up to see your solution path
4. **Known values in green**: These are already known, don't eliminate them
5. **Target in red**: This is what you're solving for

## Common Workflow

1. Launch GUI with initial equations
2. Click symbols to explore relationships
3. Right-click intermediate/complex variables
4. Select "Eliminate" to simplify
5. Repeat until only target and known values remain
6. Review history to see your solution path

## Example Session

```python
# Setup
from combine_equations import show_equation_gui
from combine_equations.kinematics_states import *
from sympy.physics.units import m, s

b = make_states_model("b", 2)
eqs = kinematics_fundamental(b, axes=['x'])

values = {
    b.states[0].pos.x: 0 * m,
    b.states[1].pos.x: 10 * m,
    b.states[0].vel.x: 5 * m/s,
    b.states[0].t: 0 * s
}

want = b.edges[0].a.x

# Launch
show_equation_gui(eqs, values, want, "Find acceleration")

# Then use mouse to:
# 1. Click symbols to highlight
# 2. Right-click to eliminate
# 3. Watch equations simplify!
```

## Integration with Existing Code

The GUI works seamlessly with your existing workflow:

```python
# Console version
from combine_equations.display_equations import display_equations_
display_equations_(eqs, values, want=target)

# GUI version (same arguments!)
from combine_equations.equation_gui import show_equation_gui
show_equation_gui(eqs, values, want=target, description="My problem")
```

## Keyboard Shortcuts

Currently all interactions are mouse-based. Future versions may add:
- `Ctrl+Z`: Undo last operation
- `Ctrl+C`: Copy current equations
- `Ctrl+S`: Save session
- `Escape`: Clear selection
