# Jupyter Equation GUI

Interactive equation viewer and manipulator for Jupyter notebooks (including JupyterLite).

## Features

- **📝 Beautiful LaTeX rendering** - Equations displayed using MathJax/KaTeX
- **🎨 Syntax highlighting** 
  - Green = known values
  - Red = target variable
  - Black = unknowns
- **💡 Interactive highlighting** - Click symbol buttons to highlight across all equations
- **⚡ Variable elimination** - Dropdown menus to eliminate or isolate variables
- **📊 History tracking** - See all transformations step-by-step

## Works In

- ✅ JupyterLab
- ✅ Classic Jupyter Notebook
- ✅ **JupyterLite** (browser-based, no installation!)
- ✅ Google Colab
- ✅ VS Code Jupyter extension

## Installation

```bash
pip install ipywidgets
```

## Quick Start

```python
from combine_equations.equation_gui_jupyter import show_equation_gui_jupyter
from combine_equations.kinematics_states import make_states_model, kinematics_fundamental
from sympy.physics.units import m, s

# Setup physics model
b = make_states_model("b", 2)
b0, b1 = b.states
b01 = b.edges[0]

# Generate equations
eqs = kinematics_fundamental(b, axes=['x'])

# Define known values and target
values = {
    b0.pos.x: 0 * m,
    b1.pos.x: 1.50 * m,
    b0.vel.x: 0 * m/s,
    b1.vel.x: 45.0 * m/s,
    b0.t: 0 * s
}
want = b01.a.x  # Find acceleration

# Show interactive GUI
gui = show_equation_gui_jupyter(eqs, values=values, want=want)
```

## Usage

1. **View equations** - Equations display with color-coded symbols
2. **Highlight symbols** - Click small buttons below equations to highlight a symbol
3. **Eliminate variables** - Use "Eliminate" dropdown for automatic elimination
4. **Manual control** - Use "Eliminate using..." for step-by-step control
5. **Track progress** - History shows all operations performed

## Comparison with Desktop GUI

| Feature | Jupyter GUI | Tkinter GUI |
|---------|------------|-------------|
| LaTeX rendering | ✅ Excellent (MathJax) | ❌ Plain text |
| Click to highlight | ✅ Button-based | ✅ Direct click |
| Right-click menus | ❌ Dropdown-based | ✅ Context menus |
| Works in browser | ✅ Yes | ❌ No |
| Shareable | ✅ Yes (notebooks) | ❌ No |
| No installation | ✅ JupyterLite | ❌ Requires Python |

## Example Notebook

See [demo_equation_gui_jupyter.ipynb](demo_equation_gui_jupyter.ipynb) for a complete example solving a kinematics problem.

## API

### show_equation_gui_jupyter(equations, values=None, want=None)

Display equations in an interactive Jupyter GUI.

**Parameters:**
- `equations` (list): List of SymPy equations
- `values` (dict, optional): Dictionary mapping symbols to known values
- `want` (Symbol, optional): Target variable to solve for

**Returns:**
- `EquationGUIJupyter`: GUI instance for programmatic manipulation

### EquationGUIJupyter.display_equations(equations, values, want, description)

Update the GUI with new equations (typically after an operation).

**Parameters:**
- `equations` (list): New list of equations
- `values` (dict): Known values
- `want` (Symbol): Target variable
- `description` (str): Description of the operation performed

## Tips

1. **Finding relationships**: Highlight a symbol to see where it appears
2. **Simplifying**: Eliminate intermediate variables you don't need
3. **Solving**: Keep eliminating until only target and known values remain
4. **Understanding**: Watch the history to build intuition about equation manipulation

## Limitations

- Click-to-highlight uses buttons rather than direct symbol clicking
- No right-click context menus (uses dropdowns instead)
- Requires ipywidgets (included with most Jupyter installations)

## Future Enhancements

Potential improvements:
- Direct symbol clicking (requires custom JavaScript)
- Undo/redo functionality
- Export history as markdown
- Copy equations to clipboard
- Side-by-side equation comparison
