# Equation GUI - Troubleshooting

## Common Issues and Solutions

### GUI Won't Launch

**Issue**: Nothing happens when running the script

**Possible Causes:**
1. **tkinter not installed**
   - Solution: `pip install tk` (or reinstall Python with tkinter)
   - Check: `python -c "import tkinter; print('OK')"`

2. **Display not available** (remote server/WSL without X)
   - Solution: Use X server (Xming, VcXsrv) or run locally

3. **Python in background**
   - Check: GUI might be hidden behind other windows

### Import Errors

**Issue**: `ModuleNotFoundError: No module named 'combine_equations'`

**Solution**: Make sure you're in the project root or add to path:
```python
import sys
sys.path.insert(0, 'src')
from combine_equations.equation_gui import show_equation_gui
```

### Symbol Click Not Working

**Issue**: Clicking symbols doesn't highlight them

**Possible Causes:**
1. **Clicking between symbols** - Click directly on the symbol text
2. **Window not responsive** - GUI might be busy processing

**Solution**: Try clicking different parts of the symbol

### Right-Click Menu Not Appearing

**Issue**: Right-click doesn't show menu

**Possible Causes:**
1. **Not on latest equations** - Can only eliminate from most recent set
2. **Clicked outside symbol** - Right-click directly on a symbol
3. **Platform-specific** - On Mac, try Ctrl+Click

**Solution**: 
- Scroll to bottom (most recent equations)
- Right-click directly on symbol text

### Elimination Fails

**Issue**: "Error eliminating symbol" message appears

**Possible Causes:**
1. **Symbol can't be solved** - Equation doesn't contain simple solution
2. **Circular dependency** - Symbol depends on itself
3. **No equations contain symbol**

**Solution**: Try eliminating a different variable first

### GUI Freezes

**Issue**: GUI becomes unresponsive

**Possible Causes:**
1. **Complex elimination** - Large equation system
2. **Infinite loop** - Circular substitution

**Solution**: 
- Close and restart
- Try simpler equation system first
- Check equations are well-formed

### Colors Not Showing

**Issue**: All text is black (no green/red)

**Possible Causes:**
1. **No values provided** - Pass `values` dict
2. **No target provided** - Pass `want` parameter
3. **Symbol mismatch** - Symbols in `values`/`want` don't match equation symbols

**Solution**: Verify arguments:
```python
print("Values:", values)
print("Want:", want)
print("Equation symbols:", eqs[0].free_symbols)
```

### History Too Long

**Issue**: GUI is slow with many operations

**Solution**: 
- Currently no limit on history
- Restart GUI for fresh start
- Future: Add "clear history" button

### Scroll Not Working

**Issue**: Can't scroll through history

**Solution**:
- Use mouse wheel
- Use scrollbar on right side
- Ensure window has focus (click inside first)

## Performance Tips

1. **Start Simple**: Test with 2-3 equations first
2. **Strategic Elimination**: Eliminate simple variables first
3. **Check Progress**: Verify each elimination before continuing
4. **Use Console First**: Test `eliminate_variable_subst()` in console first

## Debugging

### Enable Debug Output

Add to your script:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Equation Structure

```python
print("Number of equations:", len(eqs))
for i, eq in enumerate(eqs):
    print(f"Eq {i}: {eq}")
    print(f"  Symbols: {eq.free_symbols}")
```

### Verify Values/Want

```python
print("Values:")
for k, v in values.items():
    print(f"  {k}: {v}")
print(f"Want: {want}")
```

### Test Elimination Manually

```python
from combine_equations.eliminate_variable_subst import eliminate_variable_subst

# Pick a symbol
test_symbol = list(eqs[0].free_symbols)[0]
print(f"Testing elimination of: {test_symbol}")

# Try elimination
try:
    new_eqs, replacement = eliminate_variable_subst(eqs, test_symbol)
    print(f"Success! Replaced with: {replacement}")
    print(f"New equations: {len(new_eqs)}")
except Exception as e:
    print(f"Failed: {e}")
```

## Platform-Specific Issues

### Windows
- **Issue**: High DPI displays may cause blurry text
- **Solution**: Set DPI awareness in Windows settings

### macOS
- **Issue**: Right-click might not work
- **Solution**: Use Ctrl+Click instead of right-click

### Linux/WSL
- **Issue**: GUI won't display
- **Solution**: Install and configure X server
  ```bash
  export DISPLAY=:0
  ```

## Getting Help

If you encounter an issue not listed here:

1. **Check the error message** - Read it carefully
2. **Test in console** - Try operations without GUI
3. **Simplify** - Use minimal example (2 equations, 1 variable)
4. **Check versions**: 
   ```bash
   python --version  # Should be 3.7+
   pip show sympy    # Check SymPy version
   ```

## Minimal Working Example

If nothing works, try this absolute minimum:

```python
import tkinter as tk
import sympy as sp
from combine_equations.equation_gui import show_equation_gui

# Simple algebra problem
x, y = sp.symbols('x y')
eqs = [
    sp.Eq(x + y, 10),
    sp.Eq(x - y, 2)
]

show_equation_gui(eqs, values={}, want=x, description="Test")
```

If this doesn't work, the issue is likely:
- tkinter installation
- Python environment
- Display configuration

## Contact/Support

- Check documentation: `EQUATION_GUI_README.md`
- Quick reference: `GUI_QUICK_REFERENCE.md`
- Try demos: `demo_equation_gui.py` or `demo_gui_features.py`
