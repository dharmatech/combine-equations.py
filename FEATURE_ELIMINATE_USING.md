# New Feature: "Eliminate using..." 

## What's New?

You can now choose **which equation** to use when eliminating a variable! This gives you precise control over the algebraic form of your solution.

## How It Works

### Before (Auto-selection)
When you right-clicked a symbol and selected "Eliminate", the system automatically chose the "best" equation (simplest by operation count) to solve for that variable.

### Now (Manual selection)
Right-click any symbol and you'll see:

```
┌────────────────────────────────────────┐
│ Eliminate 'dt_b_0_1' (auto)            │ ← Auto-select (original behavior)
│ Eliminate 'dt_b_0_1' using...       ►  │ ← NEW! Choose specific equation
│ ────────────────────────────────────   │
│ Clear selection                        │
└────────────────────────────────────────┘
```

Hover over "Eliminate using..." to see a submenu:

```
┌──────────────────────────────────────────────────────────┐
│ Eq 1: dt_b_0_1 = -b_0_t + b_1_t                          │
│ Eq 2: v_av_x_b_0_1 = (-b_0_x + b_1_x)/dt_b_0_1          │
│ Eq 3: a_x_b_0_1 = (-b_0_v_x + b_1_v_x)/dt_b_0_1         │
└──────────────────────────────────────────────────────────┘
```

Click any equation to use it for elimination!

## Example Usage

### Scenario: Eliminate `dt_b_0_1`

**Option 1: Auto (simplest equation)**
- Right-click `dt_b_0_1`
- Select "Eliminate 'dt_b_0_1' (auto)"
- System picks: `dt_b_0_1 = -b_0_t + b_1_t` (simplest)
- Result: `dt_b_0_1 → -b_0_t + b_1_t`

**Option 2: Using specific equation**
- Right-click `dt_b_0_1`
- Hover over "Eliminate 'dt_b_0_1' using..."
- Select "Eq 2: v_av_x_b_0_1 = (-b_0_x + b_1_x)/dt_b_0_1"
- System solves Eq 2 for `dt_b_0_1`
- Result: `dt_b_0_1 → (-b_0_x + b_1_x)/v_av_x_b_0_1`

Different choice → Different algebraic form!

## Why Is This Useful?

### 1. **Different Forms**
Sometimes one form is simpler or more insightful:
```python
# Auto might give you:
a = (v1 - v0) / (t1 - t0)

# Specific equation might give you:
a = 2*(x1 - x0)/(t1 - t0)**2 - 2*v0/(t1 - t0)
```

### 2. **Avoid Complex Expressions**
Choose an equation that leads to simpler algebra:
- Use the linear equation instead of the quadratic one
- Use the equation with fewer terms

### 3. **Educational Value**
See how different elimination paths lead to different (but equivalent) results!

### 4. **Numerical Stability**
In numerical computation, some forms are more stable than others.

## Visual Comparison

### Your Example from Screenshot

**Starting equations:**
```
dt_b_0_1 = -b_0_t + b_1_t
v_av_x_b_0_1 = (-b_0_x + b_1_x)/dt_b_0_1
a_x_b_0_1 = (-b_0_v_x + b_1_v_x)/dt_b_0_1
v_av_x_b_0_1 = b_0_v_x/2 + b_1_v_x/2
```

**If you use Eq 1 to eliminate `dt_b_0_1`:**
```
▶ Eliminated dt_b_0_1 → -b_0_t + b_1_t (using: dt_b_0_1 = -b_0_t + b_1_t)

b_0_t = b_1_t - dt_b_0_1
a_x_b_0_1 = (b_0_v_x - b_1_v_x)/(b_0_t - b_1_t)
b_0_v_x/2 + b_1_v_x/2 = (b_0_x - b_1_x)/(b_0_t - b_1_t)
```

**If you use Eq 2 to eliminate `dt_b_0_1`:**
```
▶ Eliminated dt_b_0_1 → (-b_0_x + b_1_x)/v_av_x_b_0_1 (using: v_av_x_b_0_1 = (-b_0_x + b_1_x)/dt_b_0_1)

dt_b_0_1 = (-b_0_x + b_1_x)/v_av_x_b_0_1
a_x_b_0_1 = (b_0_v_x - b_1_v_x)*v_av_x_b_0_1/(-b_0_x + b_1_x)
v_av_x_b_0_1 = b_0_v_x/2 + b_1_v_x/2
```

Different but equivalent!

## Menu Features

### Equation Numbering
- **Eq 1, Eq 2, etc.** - Numbered in the order they appear in the current set
- Easy to reference: "I used Equation 3"

### Smart Filtering
- Only shows equations that contain the selected symbol
- If symbol appears in 2 equations, submenu shows only those 2
- If symbol appears in 1 equation, submenu shows only that 1

### Equation Preview
- Each menu item shows the equation (up to 50 chars)
- Longer equations are truncated with "..."
- Enough to identify which equation you want

### History Tracking
The history now shows which equation was used:
```
▶ Eliminated dt_b_0_1 → -b_0_t + b_1_t (using: dt_b_0_1 = -b_0_t + b_1...)
```

## Tips

1. **Try Both**: Use "auto" first, then undo (future feature) and try specific equation
2. **Preview First**: Look at the equations in the submenu before choosing
3. **Simpler is Better**: Choose the equation with the simplest form of the variable
4. **Check History**: Scroll up to compare different elimination paths

## Keyboard Shortcuts (Future)

Potential enhancements:
- `Ctrl+1`, `Ctrl+2`, etc. to quickly select equation 1, 2, etc.
- `Ctrl+E` to auto-eliminate
- `Ctrl+Z` to undo last elimination

## Technical Details

### What Happens Under the Hood

1. **Menu Construction**:
   - Scan all current equations
   - Filter to those containing the symbol
   - Create submenu with each equation

2. **Elimination**:
   - Solve chosen equation for symbol: `sp.solve(equation, symbol)`
   - Get replacement expression
   - Substitute into all equations: `eq.subs({symbol: replacement})`
   - Simplify and clean up

3. **Error Handling**:
   - If equation can't be solved: Show error message
   - If solution contains symbol (circular): Show warning
   - If multiple solutions: Use first one

### Comparison with Auto

| Method | Equation Selection | Description Format |
|--------|-------------------|-------------------|
| **Auto** | Simplest by `sp.count_ops()` | "Eliminated X → Y (auto)" |
| **Specific** | User-chosen | "Eliminated X → Y (using: Eq...)" |

## Example Session

```python
# Launch GUI
show_equation_gui(eqs, values, b01.a.x, "Fast Pitch")

# In GUI:
# 1. Right-click 'dt_b_0_1'
# 2. See menu with:
#    - Eliminate 'dt_b_0_1' (auto)
#    - Eliminate 'dt_b_0_1' using... ►
# 3. Hover over "using..." to see:
#    - Eq 1: dt_b_0_1 = -b_0_t + b_1_t
#    - Eq 2: v_av_x_b_0_1 = (-b_0_x + b_1_x)/dt_b_0_1
# 4. Click "Eq 2"
# 5. See result: dt_b_0_1 → (-b_0_x + b_1_x)/v_av_x_b_0_1
```

## Summary

✅ **More Control**: Choose exactly which equation to use  
✅ **Different Forms**: Explore alternative algebraic forms  
✅ **Clear History**: See which equation was used for each step  
✅ **Smart Filtering**: Only relevant equations shown  
✅ **Fallback**: "Auto" option still available  

Try it now: `python demo_gui_features.py` and right-click any symbol! 🎯
