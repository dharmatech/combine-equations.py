# Equation GUI - Architecture & Flow

## Visual Layout

```
┌────────────────────────────────────────────────────────────────┐
│  Equation Viewer & Manipulator                            [×]   │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ▶ Initial equations                                           │
│  dt_b_0_1 = -b_0_t + b_1_t                                     │
│  v_av_x_b_0_1 = (-b_0_x + b_1_x)/dt_b_0_1                      │
│  a_x_b_0_1 = (-b_0_v_x + b_1_v_x)/dt_b_0_1                     │
│  v_av_x_b_0_1 = b_0_v_x/2 + b_1_v_x/2                          │
│                                                                 │
│  ─────────────────────────────────────────────────────         │
│                                                                 │
│  ▶ Eliminated v_av_x_b_0_1 → (-b_0_x + b_1_x)/dt_b_0_1         │
│  dt_b_0_1 = -b_0_t + b_1_t                                     │
│  a_x_b_0_1 = (-b_0_v_x + b_1_v_x)/dt_b_0_1                     │
│  (-b_0_x + b_1_x)/dt_b_0_1 = b_0_v_x/2 + b_1_v_x/2             │
│                                                                 │
│  ─────────────────────────────────────────────────────         │
│                                                                 │
│  ▶ Eliminated dt_b_0_1 → -b_0_t + b_1_t                        │
│  a_x_b_0_1 = (-b_0_v_x + b_1_v_x)/(-b_0_t + b_1_t)             │
│  (-b_0_x + b_1_x)/(-b_0_t + b_1_t) = b_0_v_x/2 + b_1_v_x/2     │
│                                                                 │
│                                                           ▲  │  │
│                                                           │  │  │
│                                                           │  ▼  │
└───────────────────────────────────────────────────────────────┘
                                                           Scroll
```

## Component Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                       EquationGUI                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  State Management                                     │   │
│  │  • current_equations: List[Eq]                        │   │
│  │  • current_values: Dict[Symbol, Value]                │   │
│  │  • current_want: Symbol                               │   │
│  │  • history: List[(desc, eqs, values, want)]           │   │
│  │  • selected_symbol: Optional[Symbol]                  │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  UI Components                                        │   │
│  │  • Canvas (scrollable container)                      │   │
│  │  • Scrollbar                                          │   │
│  │  • ScrollableFrame (holds history items)              │   │
│  │    └─> HistoryItem                                    │   │
│  │        ├─> Description Label                          │   │
│  │        └─> Equation Frames                            │   │
│  │            └─> Text Widgets (interactive)             │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Event Handlers                                       │   │
│  │  • _on_mousewheel()     - Scroll                      │   │
│  │  • on_left_click()      - Highlight symbols           │   │
│  │  • on_right_click()     - Show context menu           │   │
│  │  • _eliminate_variable() - Process elimination        │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Interaction Flow

### 1. Left-Click Symbol (Highlighting)

```
User clicks symbol
       │
       ▼
Event handler identifies symbol
       │
       ▼
Update selected_symbol
       │
       ▼
Redraw entire history
       │
       ▼
All instances of symbol
highlighted in yellow
```

### 2. Right-Click Symbol (Elimination)

```
User right-clicks symbol
       │
       ▼
Check if on latest equations
       │
       ▼
Show context menu
       │
       ▼
User selects "Eliminate"
       │
       ▼
Call eliminate_variable_subst()
       │
       ▼
Get new equations + replacement
       │
       ▼
Create description
"Eliminated X → expression"
       │
       ▼
Add to history
       │
       ▼
Redraw with new equations
displayed at bottom
```

## Data Flow

```
Input: equations, values, want, description
   │
   ▼
┌────────────────────────────────┐
│  display_equations()           │
│  • Store in current state      │
│  • Add to history              │
└────────────────────────────────┘
   │
   ▼
┌────────────────────────────────┐
│  _redraw_history()             │
│  • Clear display               │
│  • For each history item:      │
│    - Draw description          │
│    - Draw equations            │
└────────────────────────────────┘
   │
   ▼
┌────────────────────────────────┐
│  _draw_equation()              │
│  • Parse equation to symbols   │
│  • Color-code each symbol      │
│  • Bind click events           │
└────────────────────────────────┘
   │
   ▼
┌────────────────────────────────┐
│  User Interaction              │
│  • Click symbols               │
│  • Right-click to eliminate    │
└────────────────────────────────┘
   │
   ▼
┌────────────────────────────────┐
│  _eliminate_variable()         │
│  • Call elimination function   │
│  • Update history              │
│  • Trigger redraw              │
└────────────────────────────────┘
   │
   ▼
Back to display loop
```

## Symbol Detection Algorithm

```
For each equation:
    Convert to string: "a_x + b_y = c_z"
    
    Extract all symbols from equation.free_symbols
    Sort by length (longest first): ["a_x", "b_y", "c_z"]
    
    Parse string character by character:
        For each position:
            Try to match each symbol:
                Check if match is complete (word boundary)
                If match:
                    Determine color (value/want/normal)
                    Add highlight if selected
                    Insert with tags
                    Bind click events
                Else:
                    Insert single character
```

## Color Tagging System

```
Text Widget Tags:
┌──────────────────────────────┐
│ Tag Name    │ Color          │
├─────────────┼────────────────┤
│ 'value'     │ #00AA00 (green)│
│ 'want'      │ #DD0000 (red)  │
│ 'normal'    │ #000000 (black)│
│ 'highlight' │ bg: #FFFF99    │
└──────────────────────────────┘

Each symbol gets tags:
- Base tag: 'value', 'want', or 'normal'
- Optional: 'highlight' if selected
- Event tag: unique per symbol instance
```

## Event Binding Strategy

```
Each symbol instance gets unique identifier:
"symbol_{history_idx}_{eq_idx}_{start_idx}"

Example:
┌────────────────────────────────────────┐
│ History Item 0, Equation 1             │
│ "b_0_x" at position 5                  │
│ Tag: "symbol_0_1_1.5"                  │
│                                         │
│ Bound events:                          │
│ • <Button-1>: on_left_click            │
│ • <Button-3>: on_right_click           │
└────────────────────────────────────────┘

This allows:
- Multiple instances of same symbol
- Each independently clickable
- Track which history item (for menu)
```

## History Management

```
History Stack:
┌────────────────────────────────┐
│ [0] Initial equations          │ ← Oldest
│ [1] Eliminated v_av            │
│ [2] Eliminated dt              │
│ [3] Eliminated a               │ ← Newest (bottom)
└────────────────────────────────┘

Operations only allowed on [3] (latest)

Display order: Top to bottom (oldest to newest)
Scrolls to bottom after each operation
```

## Integration Points

```
External Dependencies:
┌────────────────────────────────────────┐
│ from combine_equations import:         │
│ • eliminate_variable_subst             │
│ • kinematics_states (for demo)         │
│ • solve_system (for demo)              │
└────────────────────────────────────────┘

Your Code:
┌────────────────────────────────────────┐
│ # Console version                      │
│ display_equations_(eqs, values, want)  │
│                                         │
│ # GUI version (same args!)             │
│ show_equation_gui(eqs, values, want,   │
│                   description)          │
└────────────────────────────────────────┘
```

## Performance Considerations

```
Redraw Strategy:
• Entire history redrawn on each interaction
• Inefficient for very long histories (100+ items)
• Future optimization: Only redraw changed items

Symbol Parsing:
• O(n*m) where n=equation length, m=number of symbols
• Optimized by sorting symbols by length
• Fast enough for typical physics equations

Event Binding:
• Each symbol instance gets unique tag
• Could be optimized with event delegation
• Currently not a bottleneck
```

## Extension Points

```
Easy to add:
┌────────────────────────────────────────┐
│ 1. Undo/Redo:                          │
│    • Keep separate undo stack          │
│    • Pop from history on undo          │
│                                         │
│ 2. Export:                             │
│    • Add "Export" button               │
│    • Generate LaTeX from history       │
│                                         │
│ 3. Save/Load:                          │
│    • Serialize history to JSON         │
│    • Deserialize on load               │
│                                         │
│ 4. Search:                             │
│    • Add search box                    │
│    • Filter history by symbol          │
│                                         │
│ 5. Multiple Strategies:               │
│    • Add menu: Eliminate vs Solve vs.. │
│    • Branch history on choice          │
└────────────────────────────────────────┘
```
