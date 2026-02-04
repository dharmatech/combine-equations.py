"""
Interactive equation GUI for Jupyter notebooks (including JupyterLite).

Features:
- Display equations with LaTeX rendering and syntax highlighting (values in green, want in red)
- Click symbols to highlight all instances
- Dropdown menus to eliminate or isolate variables
- History/transaction-style UI showing operations and results

This module provides an ipywidgets-based GUI that works in:
- JupyterLab
- Classic Jupyter Notebook
- JupyterLite (browser-based, no installation needed)
- Google Colab
- VS Code Jupyter extension
"""

import ipywidgets as widgets
from IPython.display import display, HTML, Markdown
import sympy as sp
from typing import List, Dict, Any, Optional, Tuple
import html


class EquationGUIJupyter:
    """Interactive GUI for displaying and manipulating equations in Jupyter."""
    
    def __init__(self):
        # Current state
        self.current_equations = []
        self.current_values = {}
        self.current_want = None
        self.history = []  # List of (description, equations, values, want)
        
        # Selected symbol for highlighting
        self.selected_symbol = None
        
        # Main output area
        self.output_area = widgets.Output()
        
        # Control panel
        self.control_panel = None
        
        # Container
        self.container = None
        
    def display_equations(self, equations, values=None, want=None, description=None):
        """
        Display equations with interactive features.
        
        Args:
            equations: List of SymPy equations
            values: Dict of known values (will be colored green)
            want: Target variable (will be colored red)
            description: Optional description of this step
        """
        self.current_equations = equations
        self.current_values = values or {}
        self.current_want = want
        
        # Add to history
        if description:
            self.history.append((description, equations, values, want))
        else:
            self.history.append(("Initial equations", equations, values, want))
        
        # Create or update display
        if self.container is None:
            self._create_display()
        else:
            self._update_display()
        
    def _create_display(self):
        """Create the initial display."""
        # Control panel at the top
        self.control_panel = self._create_control_panel()
        
        # History display area
        self.output_area = widgets.Output()
        
        # Main container
        self.container = widgets.VBox([
            self.control_panel,
            widgets.HTML("<hr style='margin: 10px 0;'>"),
            self.output_area
        ])
        
        # Initial render
        self._update_display()
        
        # Display the container
        display(self.container)
        
    def _create_control_panel(self):
        """Create the control panel with interaction buttons."""
        # Title
        title = widgets.HTML("<h3 style='margin: 5px 0;'>Equation Viewer & Manipulator</h3>")
        
        # Info text
        info = widgets.HTML(
            "<p style='margin: 5px 0; color: #666; font-size: 12px;'>"
            "Click on symbols to highlight them. Use dropdowns below to manipulate equations."
            "</p>"
        )
        
        # Eliminate variable dropdown
        self.eliminate_dropdown = widgets.Dropdown(
            description='Eliminate:',
            options=['(select variable)'],
            disabled=True,
            layout=widgets.Layout(width='300px')
        )
        self.eliminate_dropdown.observe(self._on_eliminate_variable, names='value')
        
        # Eliminate using specific equation dropdown (two-stage)
        self.eliminate_using_var_dropdown = widgets.Dropdown(
            description='Eliminate:',
            options=['(select variable)'],
            disabled=True,
            layout=widgets.Layout(width='250px')
        )
        self.eliminate_using_eq_dropdown = widgets.Dropdown(
            description='Using eq:',
            options=['(select equation)'],
            disabled=True,
            layout=widgets.Layout(width='400px')
        )
        self.eliminate_using_var_dropdown.observe(self._on_eliminate_using_var_selected, names='value')
        self.eliminate_using_eq_dropdown.observe(self._on_eliminate_using_equation, names='value')
        
        eliminate_using_box = widgets.HBox([
            self.eliminate_using_var_dropdown,
            self.eliminate_using_eq_dropdown
        ])
        
        # Clear selection button
        clear_button = widgets.Button(
            description='Clear Selection',
            button_style='info',
            layout=widgets.Layout(width='150px')
        )
        clear_button.on_click(self._on_clear_selection)
        
        # Layout
        controls = widgets.VBox([
            title,
            info,
            widgets.HBox([self.eliminate_dropdown, clear_button]),
            eliminate_using_box
        ], layout=widgets.Layout(padding='10px', background_color='#f9f9f9', border='1px solid #ddd'))
        
        return controls
    
    def _update_display(self):
        """Update the display with current history."""
        with self.output_area:
            self.output_area.clear_output(wait=True)
            
            # Render all history items
            for idx, (description, equations, values, want) in enumerate(self.history):
                self._render_history_item(idx, description, equations, values, want)
        
        # Update control panel dropdowns
        self._update_control_panel()
    
    def _render_history_item(self, idx: int, description: str, equations, values, want):
        """Render a single history item."""
        # Separator between items
        if idx > 0:
            display(HTML("<hr style='margin: 20px 0; border: 1px solid #e0e0e0;'>"))
        
        # Description header
        display(HTML(
            f"<div style='font-style: italic; color: #555; margin: 10px 0; font-size: 14px;'>"
            f"▶ {html.escape(description)}</div>"
        ))
        
        # Render each equation
        for eq_idx, eq in enumerate(equations):
            if eq == True:
                continue
            self._render_equation(eq, values, want, idx, eq_idx)
    
    def _render_equation(self, eq, values, want, history_idx: int, eq_idx: int):
        """Render a single equation with syntax highlighting."""
        # Get all symbols in the equation
        all_symbols = sorted(eq.free_symbols, key=lambda s: str(s))
        
        # Build colored LaTeX
        lhs_colored = self._colorize_latex(eq.lhs, values, want, all_symbols)
        rhs_colored = self._colorize_latex(eq.rhs, values, want, all_symbols)
        
        # Create equation display
        eq_html = f"""
        <div style='margin: 8px 0; padding: 10px; background: white; border-left: 3px solid #4CAF50;'>
            <div style='font-size: 18px; font-family: "Computer Modern", "Times New Roman", serif;'>
                {lhs_colored} = {rhs_colored}
            </div>
        </div>
        """
        
        display(HTML(eq_html))
        
        # Add symbol highlight buttons for this equation (only for most recent)
        if history_idx == len(self.history) - 1:
            self._add_symbol_buttons(all_symbols)
    
    def _colorize_latex(self, expr, values, want, all_symbols) -> str:
        """Convert expression to LaTeX with color highlighting for symbols."""
        latex = sp.latex(expr)
        
        # For each symbol, wrap it in colored span (within the LaTeX)
        for symbol in all_symbols:
            symbol_str = str(symbol)
            symbol_latex = sp.latex(symbol)
            
            # Determine color
            color = 'black'
            if want is not None and symbol == want:
                color = '#CC0000'  # Red for target
            elif values is not None and symbol in values:
                color = '#00AA00'  # Green for known values
            
            # Add highlight if selected
            is_highlighted = (self.selected_symbol and symbol == self.selected_symbol)
            
            # Use \bbox for MathJax background color and \color for text color
            if is_highlighted:
                # MathJax bbox syntax: \bbox[background-color]{content}
                colored_latex = f'\\bbox[yellow,2pt]{{\\color{{{self._color_to_latex(color)}}}{{{symbol_latex}}}}}'
            else:
                # Just color the symbol
                colored_latex = f'\\color{{{self._color_to_latex(color)}}}{{{symbol_latex}}}'
            
            # Replace in LaTeX
            latex = latex.replace(symbol_latex, colored_latex)
        
        return f"\\({latex}\\)"
    
    def _color_to_latex(self, hex_color: str) -> str:
        """Convert hex color to LaTeX color name."""
        color_map = {
            '#CC0000': 'red',
            '#00AA00': 'green',
            'black': 'black'
        }
        return color_map.get(hex_color, 'black')
    
    def _add_symbol_buttons(self, symbols):
        """Add small buttons below equation for highlighting symbols."""
        # Skip if no new symbols
        if not hasattr(self, '_shown_symbol_buttons'):
            self._shown_symbol_buttons = set()
        
        new_symbols = [s for s in symbols if str(s) not in self._shown_symbol_buttons]
        if not new_symbols:
            return
        
        # Create tiny buttons for each new symbol
        buttons = []
        for symbol in new_symbols:
            btn = widgets.Button(
                description=str(symbol),
                layout=widgets.Layout(width='auto', height='25px'),
                style={'button_color': '#e0e0e0', 'font_size': '10px'}
            )
            btn.on_click(lambda b, sym=symbol: self._highlight_symbol(sym))
            buttons.append(btn)
            self._shown_symbol_buttons.add(str(symbol))
        
        if buttons:
            button_box = widgets.HBox(
                [widgets.Label('Highlight: ', layout=widgets.Layout(width='70px'))] + buttons,
                layout=widgets.Layout(margin='0 0 5px 10px')
            )
            display(button_box)
    
    def _highlight_symbol(self, symbol):
        """Highlight a symbol across all equations."""
        self.selected_symbol = symbol
        self._shown_symbol_buttons = set()  # Reset to show buttons again
        self._update_display()
    
    def _update_control_panel(self):
        """Update the control panel dropdowns based on current equations."""
        if not self.history:
            return
        
        _, current_eqs, _, _ = self.history[-1]
        
        # Get all symbols from current equations
        all_symbols = set()
        for eq in current_eqs:
            if eq != True and isinstance(eq, sp.Equality):
                all_symbols.update(eq.free_symbols)
        
        symbol_options = ['(select variable)'] + sorted([str(s) for s in all_symbols])
        
        # Update eliminate dropdown
        self.eliminate_dropdown.options = symbol_options
        self.eliminate_dropdown.disabled = len(all_symbols) == 0
        self.eliminate_dropdown.value = '(select variable)'
        
        # Update eliminate-using variable dropdown
        self.eliminate_using_var_dropdown.options = symbol_options
        self.eliminate_using_var_dropdown.disabled = len(all_symbols) == 0
        self.eliminate_using_var_dropdown.value = '(select variable)'
        
        # Reset equation dropdown
        self.eliminate_using_eq_dropdown.options = ['(select equation)']
        self.eliminate_using_eq_dropdown.disabled = True
        self.eliminate_using_eq_dropdown.value = '(select equation)'
    
    def _on_eliminate_variable(self, change):
        """Handle eliminate variable dropdown selection."""
        if change['new'] == '(select variable)':
            return
        
        symbol_str = change['new']
        
        # Find the symbol object
        symbol = self._find_symbol(symbol_str)
        if symbol is None:
            return
        
        # Eliminate the variable
        self._eliminate_variable(symbol)
        
        # Reset dropdown
        self.eliminate_dropdown.value = '(select variable)'
    
    def _on_eliminate_using_var_selected(self, change):
        """Handle variable selection for eliminate-using operation."""
        if change['new'] == '(select variable)':
            self.eliminate_using_eq_dropdown.options = ['(select equation)']
            self.eliminate_using_eq_dropdown.disabled = True
            return
        
        symbol_str = change['new']
        symbol = self._find_symbol(symbol_str)
        
        if symbol is None:
            return
        
        # Get current equations
        _, current_eqs, _, _ = self.history[-1]
        
        # Find equations containing this symbol
        equations_with_symbol = [
            (idx, eq) for idx, eq in enumerate(current_eqs)
            if eq != True and isinstance(eq, sp.Equality) and symbol in eq.free_symbols
        ]
        
        if not equations_with_symbol:
            self.eliminate_using_eq_dropdown.options = ['(no equations found)']
            self.eliminate_using_eq_dropdown.disabled = True
            return
        
        # Create options
        eq_options = ['(select equation)'] + [
            f"Eq {idx+1}: {self._format_equation_short(eq)}"
            for idx, eq in equations_with_symbol
        ]
        
        self.eliminate_using_eq_dropdown.options = eq_options
        self.eliminate_using_eq_dropdown.disabled = False
        self.eliminate_using_eq_dropdown.value = '(select equation)'
    
    def _on_eliminate_using_equation(self, change):
        """Handle equation selection for eliminate-using operation."""
        if change['new'] == '(select equation)':
            return
        
        # Parse the selection
        eq_str = change['new']
        if not eq_str.startswith('Eq '):
            return
        
        # Extract equation index
        eq_idx = int(eq_str.split(':')[0].replace('Eq ', '')) - 1
        
        # Get symbol and equation
        symbol_str = self.eliminate_using_var_dropdown.value
        symbol = self._find_symbol(symbol_str)
        
        _, current_eqs, _, _ = self.history[-1]
        source_equation = current_eqs[eq_idx]
        
        # Eliminate using this equation
        self._eliminate_using_equation(symbol, source_equation)
        
        # Reset dropdowns
        self.eliminate_using_var_dropdown.value = '(select variable)'
        self.eliminate_using_eq_dropdown.value = '(select equation)'
    
    def _on_clear_selection(self, button):
        """Handle clear selection button click."""
        self.selected_symbol = None
        self._update_display()
    
    def _find_symbol(self, symbol_str: str):
        """Find a symbol object by its string representation."""
        if not self.history:
            return None
        
        _, current_eqs, _, _ = self.history[-1]
        
        for eq in current_eqs:
            if eq != True and isinstance(eq, sp.Equality):
                for sym in eq.free_symbols:
                    if str(sym) == symbol_str:
                        return sym
        return None
    
    def _format_equation_short(self, eq, max_length=40):
        """Format an equation for display (shortened if needed)."""
        eq_str = f"{eq.lhs} = {eq.rhs}"
        if len(eq_str) > max_length:
            eq_str = eq_str[:max_length-3] + "..."
        return eq_str
    
    def _eliminate_variable(self, symbol):
        """Eliminate a variable from the current equations (auto-select best equation)."""
        from combine_equations.eliminate_variable_subst import eliminate_variable_subst
        
        # Get current equations (from latest history)
        _, current_eqs, current_values, current_want = self.history[-1]
        
        # Eliminate the variable
        try:
            new_eqs, replacement = eliminate_variable_subst(current_eqs, symbol)
            
            # Create description
            if replacement is not None:
                desc = f"Eliminated {symbol} → {replacement} (auto)"
            else:
                desc = f"Attempted to eliminate {symbol} (auto)"
            
            # Display new equations
            self.display_equations(new_eqs, current_values, current_want, desc)
            
        except Exception as e:
            desc = f"Error eliminating {symbol}: {str(e)}"
            # Show error but don't change equations
            self.history.append((desc, current_eqs, current_values, current_want))
            self._update_display()
    
    def _eliminate_using_equation(self, symbol, source_equation):
        """Eliminate a variable using a specific equation."""
        from combine_equations.eliminate_variable_subst import _safe_simplify, cleanup_equations
        
        # Get current equations (from latest history)
        _, current_eqs, current_values, current_want = self.history[-1]
        
        try:
            # Solve the specific equation for the symbol
            sols = sp.solve(source_equation, symbol)
            
            if len(sols) == 0:
                desc = f"Cannot solve equation for {symbol}"
                self.history.append((desc, current_eqs, current_values, current_want))
                self._update_display()
                return
            
            # Use the first solution
            replacement = _safe_simplify(sp.sympify(sols[0]))
            
            # Check for self-reference
            if symbol in replacement.free_symbols:
                desc = f"Cannot eliminate {symbol}: solution contains {symbol}"
                self.history.append((desc, current_eqs, current_values, current_want))
                self._update_display()
                return
            
            # Substitute into all equations
            new_eqs = [_safe_simplify(eq.subs({symbol: replacement})) for eq in current_eqs]
            new_eqs = cleanup_equations(new_eqs)
            
            # Create description showing which equation was used
            eq_str = self._format_equation_short(source_equation, max_length=30)
            desc = f"Eliminated {symbol} using: {eq_str}"
            
            # Display new equations
            self.display_equations(new_eqs, current_values, current_want, desc)
            
        except Exception as e:
            desc = f"Error eliminating {symbol}: {str(e)}"
            self.history.append((desc, current_eqs, current_values, current_want))
            self._update_display()


def show_equation_gui_jupyter(equations, values=None, want=None):
    """
    Display equations in an interactive Jupyter GUI.
    
    Works in JupyterLab, Jupyter Notebook, JupyterLite, Google Colab, and VS Code.
    
    Args:
        equations: List of SymPy equations
        values: Dict of known values (will be colored green)
        want: Target variable (will be colored red)
    
    Returns:
        EquationGUIJupyter instance (for programmatic manipulation if needed)
    
    Example:
        >>> from sympy import symbols, Eq
        >>> x, y, z = symbols('x y z')
        >>> eqs = [Eq(x + y, 10), Eq(y + z, 15), Eq(x + z, 13)]
        >>> values = {x: 5}
        >>> show_equation_gui_jupyter(eqs, values=values, want=z)
    """
    gui = EquationGUIJupyter()
    gui.display_equations(equations, values, want)
    return gui
