## Interactive Equation GUI

An interactive GUI for exploring and manipulating equations with features for variable elimination and solution tracking.

```python
from combine_equations import show_equation_gui

# Launch interactive GUI
show_equation_gui(equations, values, want, "Problem description")
```

**Features:**
- Color-coded display (green=known, red=target)
- Click symbols to highlight all instances
- Right-click to eliminate variables
- History view showing all operations

**Quick start:**
```bash
python demo_gui_features.py
```

**Documentation:** See [GUI_DOCUMENTATION_INDEX.md](GUI_DOCUMENTATION_INDEX.md) for complete guide.

---

## Testing

Install dev dependencies and run tests:

```bash
uv pip install -e ".[dev]"
uv run pytest
```
