# Equation GUI - Interactive Equation Viewer & Manipulator

An interactive GUI for visualizing and manipulating symbolic equations with features for variable elimination and equation transformation tracking.

## Features

### 1. **Equation Display with Syntax Highlighting**
- **Known values** (from `values` dict) are displayed in **green**
- **Target variable** (from `want` parameter) is displayed in **red**
- Other symbols are displayed in black

### 2. **Interactive Symbol Selection**
- **Left-click** any symbol to highlight all instances of that symbol across all equations
- Highlighted symbols appear with a yellow background
- Click elsewhere or select another symbol to change selection

### 3. **Variable Elimination**
- **Right-click** any symbol to open a context menu
- Select **"Eliminate"** to remove that variable from the equation system
- The GUI uses `eliminate_variable_subst()` to perform substitution-based elimination
- Shows what the variable was replaced with

### 4. **History/Transaction UI**
- All operations are recorded in a scrollable history
- Each step shows:
  - A description of the operation (e.g., "Eliminated v_av_x_b_0_1 → ...")
  - The resulting set of equations
- History grows downward like a terminal
- Scroll through to see previous states

## Usage

### Basic Usage

```python
from combine_equations.equation_gui import show_equation_gui
import sympy as sp

# Your equations
x, y, z = sp.symbols('x y z')
eq1 = sp.Eq(x + y, 10)
eq2 = sp.Eq(x - y, 2)

# Known values (optional)
values = {}

# Target variable (optional)
want = x

# Launch GUI
show_equation_gui([eq1, eq2], values, want, "My Problem")
```

### With Kinematics Example

```python
from combine_equations.equation_gui import show_equation_gui
from combine_equations.kinematics_states import make_states_model, kinematics_fundamental
from sympy.physics.units import m, s

# Setup problem
b = make_states_model("b", 2)
b0, b1 = b.states
b01 = b.edges[0]
eqs = kinematics_fundamental(b, axes=['x'])

# Known values
values = {
    b0.pos.x: 0 * m,
    b1.pos.x: 1.50 * m,
    b0.vel.x: 0 * m/s,
    b1.vel.x: 45.0 * m/s,
    b0.t: 0 * s
}

# Launch GUI
show_equation_gui(eqs, values, b01.a.x, "Fast Pitch Problem")
```

## Running the Demos

### Demo 1: Standalone Demo
```bash
python demo_equation_gui.py
```

### Demo 2: Fast Pitch Problem
```bash
python examples/up/ch2/exercises/2.21/up-exercise-2.21-001-gui.py
```

## Implementation Details

### Architecture
- Built with **tkinter** (Python's standard GUI library)
- Uses `tk.Text` widgets for rich text formatting
- Scrollable canvas for unlimited history
- Tag-based event binding for click interactions

### Key Components

1. **EquationGUI class**: Main GUI controller
   - Manages history stack
   - Handles symbol highlighting
   - Processes elimination operations

2. **Symbol Detection**: Parses equation strings to identify clickable symbols

3. **Event Binding**: Each symbol instance gets unique click handlers

4. **Color Coding**:
   - Green (`#00AA00`): Known values
   - Red (`#DD0000`): Target variable
   - Yellow background (`#FFFF99`): Selected/highlighted symbol

### Integration Points

The GUI integrates with your existing codebase:
- `eliminate_variable_subst()`: For variable elimination
- `display_equations_()`: Mimics the same color scheme
- Works with any SymPy equations

## Workflow Example

1. **Initial Display**: Equations appear with color coding
2. **Explore**: Click symbols to see where they appear
3. **Eliminate**: Right-click a complex term like `v_av_x_b_0_1`
4. **Review**: See the substitution and simplified equations
5. **Repeat**: Continue eliminating until you reach your target
6. **History**: Scroll up to see all steps taken

## Tips

- Right-click operations only work on the **most recent** equation set
- Select symbols you want to eliminate carefully
- The history is preserved for the entire session
- Use mouse wheel or scrollbar to navigate history
- Clear selection from the context menu if needed

## Requirements

- Python 3.7+
- tkinter (usually included with Python)
- sympy
- Your existing `combine_equations` package

## Future Enhancements (Potential)

- Export history to LaTeX or PDF
- Undo/redo functionality
- Save/load sessions
- Multiple elimination strategies
- Step-by-step solution path finding
- Copy equations to clipboard
