"""
GUI for displaying and manipulating equations with interactive features.

Features:
- Display equations with syntax highlighting (values in green, want in red)
- Click symbols to highlight all instances
- Right-click symbols to eliminate variables
- History/transaction-style UI showing operations and results
"""

import tkinter as tk
from tkinter import ttk, font as tkfont
import sympy as sp
import re
from typing import List, Dict, Any, Optional, Tuple


class EquationGUI:
    """Interactive GUI for displaying and manipulating equations."""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Equation Viewer & Manipulator")
        self.root.geometry("1000x700")
        
        # Current state
        self.current_equations = []
        self.current_values = {}
        self.current_want = None
        self.history = []  # List of (description, equations, values, want)
        
        # Selected symbol for highlighting
        self.selected_symbol = None
        
        # Setup GUI
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup the user interface."""
        # Main container with scrollbar
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollable canvas
        self.canvas = tk.Canvas(main_frame, bg='white')
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Enable mouse wheel scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Fonts
        self.equation_font = tkfont.Font(family="Courier New", size=12)
        self.description_font = tkfont.Font(family="Arial", size=10, slant="italic")
        
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling."""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
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
        
        # Redraw entire history
        self._redraw_history()
        
    def _redraw_history(self):
        """Redraw the entire history."""
        # Clear current display
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Draw each history item
        for idx, (description, equations, values, want) in enumerate(self.history):
            self._draw_history_item(idx, description, equations, values, want)
        
        # Scroll to bottom
        self.root.after(100, lambda: self.canvas.yview_moveto(1.0))
        
    def _draw_history_item(self, idx: int, description: str, equations, values, want):
        """Draw a single history item."""
        # Separator
        if idx > 0:
            sep = ttk.Separator(self.scrollable_frame, orient='horizontal')
            sep.pack(fill=tk.X, padx=20, pady=10)
        
        # Container for this item
        item_frame = ttk.Frame(self.scrollable_frame)
        item_frame.pack(fill=tk.X, padx=20, pady=5)
        
        # Description
        desc_label = tk.Label(
            item_frame,
            text=f"▶ {description}",
            font=self.description_font,
            fg='#555555',
            bg='white',
            anchor='w'
        )
        desc_label.pack(fill=tk.X, pady=(0, 5))
        
        # Equations
        for eq_idx, eq in enumerate(equations):
            if eq == True:
                continue
            self._draw_equation(item_frame, eq, values, want, idx, eq_idx)
        
    def _draw_equation(self, parent, eq, values, want, history_idx: int, eq_idx: int):
        """Draw a single equation with interactive features."""
        # Frame for this equation
        eq_frame = tk.Frame(parent, bg='white')
        eq_frame.pack(fill=tk.X, pady=2)
        
        # Convert equation to string parts
        lhs_str = str(eq.lhs)
        rhs_str = str(eq.rhs)
        
        # Extract all symbols
        all_symbols = self._extract_symbols(eq)
        
        # Create text widget for the equation
        text_widget = tk.Text(
            eq_frame,
            height=1,
            font=self.equation_font,
            bg='white',
            relief=tk.FLAT,
            wrap=tk.NONE,
            cursor='hand2'
        )
        text_widget.pack(fill=tk.X)
        
        # Insert LHS
        self._insert_expression(text_widget, lhs_str, values, want, all_symbols, history_idx, eq_idx, 'lhs')
        
        # Insert equals sign
        text_widget.insert(tk.END, ' = ', 'normal')
        
        # Insert RHS
        self._insert_expression(text_widget, rhs_str, values, want, all_symbols, history_idx, eq_idx, 'rhs')
        
        # Make text widget read-only
        text_widget.config(state=tk.DISABLED)
        
        # Configure tags for colors
        text_widget.tag_config('value', foreground='#00AA00')  # Green
        text_widget.tag_config('want', foreground='#DD0000')  # Red
        text_widget.tag_config('normal', foreground='#000000')  # Black
        text_widget.tag_config('highlight', background='#FFFF99')  # Yellow highlight
        
    def _insert_expression(self, text_widget, expr_str: str, values, want, 
                          all_symbols: List[str], history_idx: int, eq_idx: int, side: str):
        """Insert an expression into the text widget with proper formatting."""
        # Parse expression and identify symbols
        pos = 0
        
        # Sort symbols by length (longest first) to avoid partial matches
        sorted_symbols = sorted(all_symbols, key=len, reverse=True)
        
        while pos < len(expr_str):
            # Try to match a symbol
            matched = False
            for symbol in sorted_symbols:
                if expr_str[pos:pos+len(symbol)] == symbol:
                    # Check if this is a complete symbol (not part of a longer one)
                    if self._is_complete_symbol(expr_str, pos, len(symbol)):
                        # Determine tag
                        tag = 'normal'
                        symbol_obj = self._str_to_symbol(symbol, all_symbols)
                        
                        if want is not None and symbol_obj == want:
                            tag = 'want'
                        elif values is not None and symbol_obj in values:
                            tag = 'value'
                        
                        # Add highlight if selected
                        tags = [tag]
                        if self.selected_symbol and str(symbol_obj) == str(self.selected_symbol):
                            tags.append('highlight')
                        
                        # Insert with tag
                        start_idx = text_widget.index(tk.INSERT)
                        text_widget.insert(tk.END, symbol, tags)
                        end_idx = text_widget.index(tk.INSERT)
                        
                        # Bind click events
                        self._bind_symbol_events(
                            text_widget, start_idx, end_idx,
                            symbol_obj, history_idx, eq_idx
                        )
                        
                        pos += len(symbol)
                        matched = True
                        break
            
            if not matched:
                # Insert single character
                text_widget.insert(tk.END, expr_str[pos], 'normal')
                pos += 1
                
    def _is_complete_symbol(self, expr_str: str, pos: int, length: int) -> bool:
        """Check if the symbol at position is complete (not part of a longer identifier)."""
        # Check character before
        if pos > 0:
            prev_char = expr_str[pos-1]
            if prev_char.isalnum() or prev_char == '_':
                return False
        
        # Check character after
        if pos + length < len(expr_str):
            next_char = expr_str[pos + length]
            if next_char.isalnum() or next_char == '_':
                return False
        
        return True
    
    def _extract_symbols(self, eq) -> List[str]:
        """Extract all symbols from an equation as strings."""
        symbols = eq.free_symbols
        return sorted([str(s) for s in symbols], key=len, reverse=True)
    
    def _str_to_symbol(self, symbol_str: str, all_symbols: List[str]) -> sp.Symbol:
        """Convert a string back to a SymPy symbol."""
        # Try to find in current equation's free symbols
        for eq in self.current_equations:
            for sym in eq.free_symbols:
                if str(sym) == symbol_str:
                    return sym
        # Fallback: create new symbol
        return sp.Symbol(symbol_str)
    
    def _bind_symbol_events(self, text_widget, start_idx, end_idx, 
                           symbol, history_idx: int, eq_idx: int):
        """Bind click events to a symbol."""
        # Left click: highlight
        def on_left_click(event):
            self.selected_symbol = symbol
            self._redraw_history()
            
        # Right click: context menu
        def on_right_click(event):
            # Only allow operations on the most recent equations
            if history_idx == len(self.history) - 1:
                self._show_context_menu(event, symbol)
        
        # Bind to the tag range
        tag_name = f"symbol_{history_idx}_{eq_idx}_{start_idx}"
        text_widget.tag_add(tag_name, start_idx, end_idx)
        text_widget.tag_bind(tag_name, "<Button-1>", on_left_click)
        text_widget.tag_bind(tag_name, "<Button-3>", on_right_click)
        
    def _show_context_menu(self, event, symbol):
        """Show context menu for a symbol."""
        menu = tk.Menu(self.root, tearoff=0)
        
        # Add "Eliminate" option (auto-select best equation)
        menu.add_command(
            label=f"Eliminate '{symbol}' (auto)",
            command=lambda: self._eliminate_variable(symbol)
        )
        
        # Add "Eliminate using..." submenu
        _, current_eqs, _, _ = self.history[-1]
        equations_with_symbol = [
            (idx, eq) for idx, eq in enumerate(current_eqs)
            if eq != True and isinstance(eq, sp.Equality) and symbol in eq.free_symbols
        ]
        
        if len(equations_with_symbol) > 0:
            eliminate_menu = tk.Menu(menu, tearoff=0)
            for idx, eq in equations_with_symbol:
                # Create a shortened display of the equation
                eq_str = self._format_equation_for_menu(eq, max_length=50)
                eliminate_menu.add_command(
                    label=f"Eq {idx+1}: {eq_str}",
                    command=lambda eq=eq, sym=symbol: self._eliminate_using_equation(sym, eq)
                )
            menu.add_cascade(label=f"Eliminate '{symbol}' using...", menu=eliminate_menu)
        
        # Add "Isolate variable in..." submenu
        if len(equations_with_symbol) > 0:
            isolate_menu = tk.Menu(menu, tearoff=0)
            for idx, eq in equations_with_symbol:
                # Create a shortened display of the equation
                eq_str = self._format_equation_for_menu(eq, max_length=50)
                isolate_menu.add_command(
                    label=f"Eq {idx+1}: {eq_str}",
                    command=lambda eq=eq, sym=symbol, eq_idx=idx: self._isolate_variable(sym, eq, eq_idx)
                )
            menu.add_cascade(label=f"Isolate '{symbol}' in...", menu=isolate_menu)
        
        menu.add_separator()
        menu.add_command(label="Clear selection", command=self._clear_selection)
        
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
    
    def _format_equation_for_menu(self, eq, max_length=50):
        """Format an equation for display in menu (shortened if needed)."""
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
            self._redraw_history()
    
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
                self._redraw_history()
                return
            
            # Use the first solution
            replacement = _safe_simplify(sp.sympify(sols[0]))
            
            # Check for self-reference
            if symbol in replacement.free_symbols:
                desc = f"Cannot eliminate {symbol}: solution contains {symbol}"
                self.history.append((desc, current_eqs, current_values, current_want))
                self._redraw_history()
                return
            
            # Substitute into all equations
            new_eqs = [_safe_simplify(eq.subs({symbol: replacement})) for eq in current_eqs]
            new_eqs = cleanup_equations(new_eqs)
            
            # Create description showing which equation was used
            source_eq_str = self._format_equation_for_menu(source_equation, max_length=40)
            desc = f"Eliminated {symbol} → {replacement} (using: {source_eq_str})"
            
            # Display new equations
            self.display_equations(new_eqs, current_values, current_want, desc)
            
        except Exception as e:
            desc = f"Error eliminating {symbol} using specified equation: {str(e)}"
            self.history.append((desc, current_eqs, current_values, current_want))
            self._redraw_history()
    
    def _isolate_variable(self, symbol, source_equation, eq_index):
        """Isolate a variable in a specific equation (rewrite it as symbol = ...)."""
        from combine_equations.misc import isolate_variable
        
        # Get current equations (from latest history)
        _, current_eqs, current_values, current_want = self.history[-1]
        
        try:
            # Isolate the variable in the equation
            isolated_eq = isolate_variable(source_equation, symbol)
            
            # Replace the original equation with the isolated form
            new_eqs = list(current_eqs)
            new_eqs[eq_index] = isolated_eq
            
            # Create description
            source_eq_str = self._format_equation_for_menu(source_equation, max_length=40)
            desc = f"Isolated {symbol} in Eq {eq_index+1} (was: {source_eq_str})"
            
            # Display new equations
            self.display_equations(new_eqs, current_values, current_want, desc)
            
        except ValueError as e:
            desc = f"Cannot isolate {symbol}: {str(e)}"
            self.history.append((desc, current_eqs, current_values, current_want))
            self._redraw_history()
        except Exception as e:
            desc = f"Error isolating {symbol}: {str(e)}"
            self.history.append((desc, current_eqs, current_values, current_want))
            self._redraw_history()
            
    def _clear_selection(self):
        """Clear symbol selection."""
        self.selected_symbol = None
        self._redraw_history()


def show_equation_gui(equations, values=None, want=None, description="Initial equations"):
    """
    Launch the equation GUI.
    
    Args:
        equations: List of SymPy equations
        values: Dict of known values
        want: Target variable
        description: Description of this equation set
    """
    root = tk.Tk()
    gui = EquationGUI(root)
    gui.display_equations(equations, values, want, description)
    root.mainloop()


if __name__ == "__main__":
    # Example usage
    from combine_equations.kinematics_states import make_states_model, kinematics_fundamental
    from sympy.physics.units import m, s
    
    # Create a simple example
    b = make_states_model("b", 2)
    b0, b1 = b.states
    b01 = b.edges[0]
    eqs = kinematics_fundamental(b, axes=['x'])
    
    values = {}
    values[b0.pos.x] = 0 * m
    values[b1.pos.x] = 1.50 * m
    values[b0.vel.x] = 0 * m/s
    values[b1.vel.x] = 45.0 * m/s
    values[b0.t] = 0 * s
    
    show_equation_gui(eqs, values, b01.a.x, "Example: Fast Pitch")
