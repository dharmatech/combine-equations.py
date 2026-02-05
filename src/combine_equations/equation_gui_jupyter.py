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

__version__ = "1.3.0"

import ipywidgets as widgets
from IPython.display import display, HTML, Markdown
import sympy as sp
from typing import List, Dict, Any, Optional, Tuple
import html
import re


class EquationGUIJupyter:
    """Interactive GUI for displaying and manipulating equations in Jupyter."""
    
    def __init__(self):
        # Generate unique instance ID
        import time
        self.instance_id = f"eqgui_{int(time.time() * 1000000)}"
        
        # Current state
        self.current_equations = []
        self.current_values = {}
        self.current_want = None
        self.history = []  # List of (description, equations, values, want)
        
        # Selected symbol for highlighting
        self.selected_symbol = None
        
        # Hidden widget for JavaScript-Python communication
        self.click_bridge = widgets.Text(value='', description='')
        self.click_bridge.layout.display = 'none'
        self.click_bridge.observe(self._on_symbol_clicked, names='value')
        
        # Hidden widget for context menu commands
        self.context_menu_bridge = widgets.Text(value='', description='')
        self.context_menu_bridge.layout.display = 'none'
        self.context_menu_bridge.observe(self._on_context_menu_command, names='value')
        
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
        
        # Main container (include hidden bridges)
        self.container = widgets.VBox([
            self.control_panel,
            widgets.HTML("<hr style='margin: 10px 0;'>"),
            self.click_bridge,  # Hidden widget for click JS communication
            self.context_menu_bridge,  # Hidden widget for context menu JS communication
            self.output_area
        ])
        
        # Add instance ID as CSS class to container for JavaScript to find
        self.container.add_class(f'eqgui-instance-{self.instance_id}')
        
        # Initial render
        self._update_display()
        
        # Display the container
        display(self.container)
        
    def _create_control_panel(self):
        """Create the control panel with interaction buttons."""
        # Title with version
        title = widgets.HTML(
            f"<h3 style='margin: 5px 0;'>Equation Viewer & Manipulator "
            f"<span style='font-size:10px; color:#888;'>(v{__version__})</span></h3>"
        )
        
        # Info text
        info = widgets.HTML(
            "<p style='margin: 5px 0; color: #666; font-size: 12px;'>"
            "<b>Left-click symbols</b> to highlight them. "
            "<b>Right-click symbols</b> for elimination/isolation options."
            "</p>"
        )
        
        # Layout
        controls = widgets.VBox([
            title,
            info
        ], layout=widgets.Layout(padding='10px', background_color='#f9f9f9', border='1px solid #ddd'))
        
        return controls
    
    def _update_display(self):
        """Update the display with current history."""
        with self.output_area:
            self.output_area.clear_output(wait=True)
            
            # Inject JavaScript once at the beginning
            self._inject_javascript()
            
            # Render all history items
            for idx, (description, equations, values, want) in enumerate(self.history):
                self._render_history_item(idx, description, equations, values, want)
    
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
        """Render a single equation with syntax highlighting and clickable symbols."""
        # Build HTML for each side using recursive expression-to-HTML converter
        lhs_html = self._expr_to_html(eq.lhs, values, want)
        rhs_html = self._expr_to_html(eq.rhs, values, want)
        
        # Create equation display with unique ID
        eq_id = f"eq_{history_idx}_{eq_idx}"
        eq_html = f"""
        <div id="{eq_id}" class="equation-row" style='margin: 8px 0; padding: 10px; background: white; border-left: 3px solid #4CAF50;'
             data-instance-id="{self.instance_id}">
            <span style='font-size: 18px; display: inline-flex; align-items: center; flex-wrap: wrap; gap: 0 4px;'>
                {lhs_html}
                <span style="margin: 0 4px;">=</span>
                {rhs_html}
            </span>
        </div>
        """
        
        display(HTML(eq_html))
    
    # ── Recursive expression → HTML converter ──────────────────────────
    
    def _expr_to_html(self, expr, values, want) -> str:
        """Recursively convert a SymPy expression to HTML with per-symbol click targets.
        
        Each symbol is rendered as its own \\(LaTeX\\) inside a <span class="eqsym">
        with a data-sym attribute. Equation structure (fractions, sums, products,
        powers) is rendered using HTML/CSS so click detection is trivially correct.
        """
        # --- Atoms -------------------------------------------------------
        if isinstance(expr, sp.Symbol):
            return self._symbol_to_html(expr, values, want)
        
        if isinstance(expr, sp.Number):
            return self._number_to_html(expr)
        
        # --- Addition  a + b - c  ----------------------------------------
        if isinstance(expr, sp.Add):
            return self._add_to_html(expr, values, want)
        
        # --- Multiplication / Division -----------------------------------
        if isinstance(expr, sp.Mul):
            return self._mul_to_html(expr, values, want)
        
        # --- Powers / Reciprocals ----------------------------------------
        if isinstance(expr, sp.Pow):
            return self._pow_to_html(expr, values, want)
        
        # --- Fallback: render the whole thing as LaTeX (no click targets) -
        return f'<span>\\({sp.latex(expr)}\\)</span>'
    
    def _symbol_to_html(self, sym: sp.Symbol, values, want) -> str:
        """Render a single symbol as a clickable HTML span wrapping its LaTeX."""
        sym_str = str(sym)
        sym_latex = sp.latex(sym)
        
        # Determine color
        color = 'black'
        if want is not None and sym == want:
            color = '#CC0000'
        elif values is not None and sym in values:
            color = '#00AA00'
        
        # Highlight if selected
        bg = 'background:yellow;' if (self.selected_symbol and sym == self.selected_symbol) else ''
        
        return (
            f'<span class="eqsym" data-sym="{html.escape(sym_str)}" '
            f'data-instance-id="{self.instance_id}" '
            f'style="cursor:pointer;color:{color};{bg}display:inline-block;padding:0 1px;">'
            f'\\({sym_latex}\\)</span>'
        )
    
    def _number_to_html(self, num) -> str:
        """Render a numeric value."""
        return f'<span>\\({sp.latex(num)}\\)</span>'
    
    def _add_to_html(self, expr: sp.Add, values, want) -> str:
        """Render addition: a + b - c."""
        terms = expr.as_ordered_terms()
        parts = []
        for i, term in enumerate(terms):
            if i == 0:
                # First term: include its sign only if negative
                coeff = self._leading_coeff(term)
                if coeff is not None and coeff < 0:
                    parts.append('<span style="margin:0 2px;">−</span>')
                    parts.append(self._expr_to_html(-term, values, want))
                else:
                    parts.append(self._expr_to_html(term, values, want))
            else:
                coeff = self._leading_coeff(term)
                if coeff is not None and coeff < 0:
                    parts.append('<span style="margin:0 2px;">−</span>')
                    parts.append(self._expr_to_html(-term, values, want))
                else:
                    parts.append('<span style="margin:0 2px;">+</span>')
                    parts.append(self._expr_to_html(term, values, want))
        return '<span style="display:inline-flex;align-items:center;">' + ''.join(parts) + '</span>'
    
    def _leading_coeff(self, expr):
        """Get the leading numeric coefficient of an expression, or None."""
        if isinstance(expr, sp.Number):
            return float(expr)
        if isinstance(expr, sp.Mul):
            first = expr.args[0]
            if isinstance(first, sp.Number):
                return float(first)
        return None
    
    def _mul_to_html(self, expr: sp.Mul, values, want) -> str:
        """Render multiplication, detecting fractions (negative powers)."""
        numer, denom = expr.as_numer_denom()
        
        if denom != sp.S.One:
            # It's a fraction
            numer_html = self._expr_to_html(numer, values, want)
            denom_html = self._expr_to_html(denom, values, want)
            return self._fraction_html(numer_html, denom_html)
        
        # Regular product: factor out numeric coefficient, render rest
        coeff, rest = expr.as_coeff_Mul()
        
        factors = []
        if coeff != 1 and coeff != -1:
            factors.append(self._number_to_html(abs(coeff)))
        
        # Get the remaining factors
        if rest == sp.S.One:
            pass  # coeff only
        elif isinstance(rest, sp.Mul):
            for factor in rest.args:
                factors.append(self._expr_to_html(factor, values, want))
        else:
            factors.append(self._expr_to_html(rest, values, want))
        
        if not factors:
            factors.append(self._number_to_html(abs(coeff)))
        
        # Join factors with thin spaces (implicit multiplication)
        separator = '<span style="margin:0 1px;"></span>'
        return separator.join(factors)
    
    def _pow_to_html(self, expr: sp.Pow, values, want) -> str:
        """Render powers: x**2, x**(-1) → 1/x, etc."""
        base, exp = expr.args
        
        if exp == sp.S.NegativeOne:
            # 1/base → fraction
            numer_html = self._number_to_html(sp.S.One)
            denom_html = self._expr_to_html(base, values, want)
            return self._fraction_html(numer_html, denom_html)
        
        if isinstance(exp, sp.Number) and exp < 0:
            # base^(-n) → 1 / base^n
            numer_html = self._number_to_html(sp.S.One)
            denom_html = self._expr_to_html(sp.Pow(base, -exp), values, want)
            return self._fraction_html(numer_html, denom_html)
        
        if isinstance(exp, sp.Rational) and not isinstance(exp, sp.Integer):
            # Fractional exponent: render as LaTeX fallback for roots etc.
            return f'<span>\\({sp.latex(expr)}\\)</span>'
        
        # Regular power: base^exp
        base_html = self._expr_to_html(base, values, want)
        exp_html = self._expr_to_html(exp, values, want)
        
        # Wrap base in parens if it's a compound expression
        if isinstance(base, (sp.Add, sp.Mul)):
            base_html = f'<span>(</span>{base_html}<span>)</span>'
        
        return (
            f'<span style="display:inline-flex;align-items:baseline;">'
            f'{base_html}'
            f'<sup style="font-size:0.7em;">{exp_html}</sup>'
            f'</span>'
        )
    
    def _fraction_html(self, numer_html: str, denom_html: str) -> str:
        """Render a fraction using HTML/CSS."""
        return (
            '<span class="eq-frac" style="display:inline-flex;flex-direction:column;'
            'align-items:center;vertical-align:middle;margin:0 2px;">'
            f'<span style="padding:1px 4px;border-bottom:1.2px solid currentColor;'
            f'display:inline-flex;align-items:center;justify-content:center;">{numer_html}</span>'
            f'<span style="padding:1px 4px;'
            f'display:inline-flex;align-items:center;justify-content:center;">{denom_html}</span>'
            '</span>'
        )
    
    def _inject_javascript(self):
        """Inject JavaScript for handling symbol clicks and context menu using event delegation.
        
        With the new per-symbol HTML approach, each symbol lives in its own
        <span class="eqsym" data-sym="symbol_name"> element.  Click detection
        is trivial: walk up from the event target to find the nearest .eqsym
        ancestor and read its data-sym attribute.  No text-matching or position
        heuristics needed.
        """
        
        # First inject CSS for context menu and equation styles
        self._inject_context_menu_css()
        
        js_code = """
        <script>
        // Only add listener once
        if (!window._equationGuiListenerAdded) {
            window._equationGuiListenerAdded = true;
            
            window._activeContextMenu = null;
            
            // ── Helper: find the nearest .eqsym ancestor (or self) ──────
            function findEqSym(target) {
                var el = target;
                for (var i = 0; i < 20 && el; i++) {
                    if (el.classList && el.classList.contains('eqsym')) {
                        return el;
                    }
                    el = el.parentElement;
                }
                return null;
            }
            
            // ── Helper: find the .equation-row ancestor to get eq index ─
            function findEquationRow(target) {
                var el = target;
                for (var i = 0; i < 30 && el; i++) {
                    if (el.classList && el.classList.contains('equation-row')) {
                        return el;
                    }
                    el = el.parentElement;
                }
                return null;
            }
            
            // ── Helper: send value to hidden bridge widget ──────────────
            function sendToBridge(instanceId, bridgeIndex, value) {
                // Find instance container
                var container = null;
                if (instanceId) {
                    var containers = document.querySelectorAll('.eqgui-instance-' + instanceId);
                    if (containers.length > 0) container = containers[0];
                }
                if (!container) return false;
                
                var inputs = container.querySelectorAll('input[type="text"]');
                var hiddenInputs = [];
                for (var i = 0; i < inputs.length; i++) {
                    var p = inputs[i].parentElement;
                    if (p && p.style && p.style.display === 'none') {
                        hiddenInputs.push(inputs[i]);
                    }
                }
                if (hiddenInputs.length > bridgeIndex) {
                    var input = hiddenInputs[bridgeIndex];
                    input.value = value;
                    input.dispatchEvent(new Event('input', { bubbles: true }));
                    input.dispatchEvent(new Event('change', { bubbles: true }));
                    return true;
                }
                return false;
            }
            
            // ── Left-click: highlight symbol ────────────────────────────
            document.addEventListener('click', function(event) {
                // Close any context menu
                if (window._activeContextMenu) {
                    window._activeContextMenu.remove();
                    window._activeContextMenu = null;
                }
                
                var symSpan = findEqSym(event.target);
                if (!symSpan) return;
                
                var symbolStr = symSpan.getAttribute('data-sym');
                var instanceId = symSpan.getAttribute('data-instance-id');
                if (!symbolStr || !instanceId) return;
                
                sendToBridge(instanceId, 0, symbolStr + '_' + Date.now());
                console.log('Symbol click:', symbolStr);
            });
            
            // ── Right-click: context menu ───────────────────────────────
            document.addEventListener('contextmenu', function(event) {
                var symSpan = findEqSym(event.target);
                if (!symSpan) return true;
                
                event.preventDefault();
                event.stopPropagation();
                event.stopImmediatePropagation();
                
                var symbolStr = symSpan.getAttribute('data-sym');
                var instanceId = symSpan.getAttribute('data-instance-id');
                if (!symbolStr || !instanceId) return false;
                
                // Store for context menu commands
                window._lastClickedInstanceId = instanceId;
                
                // Get equation index from .equation-row ancestor
                var eqRow = findEquationRow(symSpan);
                var eqIdx = null;
                if (eqRow && eqRow.id) {
                    var parts = eqRow.id.split('_');
                    if (parts.length >= 3) eqIdx = parseInt(parts[2]);
                }
                
                showContextMenu(event.clientX, event.clientY, symbolStr, eqIdx);
                return false;
            }, true);
            
            // ── Context menu builder ────────────────────────────────────
            function showContextMenu(x, y, symbol, eqIdx) {
                if (window._activeContextMenu) {
                    window._activeContextMenu.remove();
                }
                
                var menu = document.createElement('div');
                menu.className = 'equation-context-menu';
                menu.style.left = x + 'px';
                menu.style.top = y + 'px';
                menu.oncontextmenu = function(e) { e.preventDefault(); return false; };
                
                addMenuItem(menu, "Eliminate '" + symbol + "' (auto)", 'eliminate_auto:' + symbol, false);
                addMenuItemWithSubmenu(menu, "Eliminate '" + symbol + "' using...", symbol, x, y, 'eliminate');
                menu.appendChild(createSeparator());
                
                if (eqIdx !== null) {
                    addMenuItem(menu, "Isolate '" + symbol + "'", 'isolate:' + symbol + ':' + eqIdx, false);
                }
                addMenuItemWithSubmenu(menu, "Isolate '" + symbol + "' in...", symbol, x, y, 'isolate');
                menu.appendChild(createSeparator());
                addMenuItem(menu, "Clear selection", 'clear_selection', false);
                
                document.body.appendChild(menu);
                
                var r = menu.getBoundingClientRect();
                if (r.right > window.innerWidth) menu.style.left = (x - r.width) + 'px';
                if (r.bottom > window.innerHeight) menu.style.top = (y - r.height) + 'px';
                
                window._activeContextMenu = menu;
            }
            
            function addMenuItem(menu, label, command, hasSubmenu) {
                var item = document.createElement('div');
                item.className = 'equation-context-menu-item';
                if (hasSubmenu) {
                    item.innerHTML = label + ' <span style="float:right;margin-left:20px;">▶</span>';
                } else {
                    item.textContent = label;
                    item.onclick = function(e) {
                        e.stopPropagation();
                        sendContextMenuCommand(command);
                        menu.remove();
                        window._activeContextMenu = null;
                    };
                }
                menu.appendChild(item);
                return item;
            }
            
            function addMenuItemWithSubmenu(parentMenu, label, symbol, parentX, parentY, action) {
                var item = addMenuItem(parentMenu, label, '', true);
                var submenu = null;
                
                item.onclick = function(e) {
                    e.stopPropagation();
                    if (submenu) { submenu.remove(); submenu = null; return; }
                    
                    getEquationsWithSymbol(symbol, function(equations) {
                        if (equations.length === 0) return;
                        
                        submenu = document.createElement('div');
                        submenu.className = 'equation-context-menu';
                        
                        var itemRect = item.getBoundingClientRect();
                        var parentRect = parentMenu.getBoundingClientRect();
                        submenu.style.left = (parentRect.right + 2) + 'px';
                        submenu.style.top = itemRect.top + 'px';
                        
                        for (var i = 0; i < equations.length; i++) {
                            var eq = equations[i];
                            var command = action + '_using:' + symbol + ':' + eq.index;
                            var si = document.createElement('div');
                            si.className = 'equation-context-menu-item';
                            si.textContent = 'Eq ' + (eq.index + 1) + ': ' + eq.display;
                            (function(cmd) {
                                si.onclick = function(ev) {
                                    ev.stopPropagation();
                                    sendContextMenuCommand(cmd);
                                    if (submenu) { submenu.remove(); submenu = null; }
                                    if (parentMenu) parentMenu.remove();
                                    window._activeContextMenu = null;
                                };
                            })(command);
                            submenu.appendChild(si);
                        }
                        
                        document.body.appendChild(submenu);
                        var sr = submenu.getBoundingClientRect();
                        if (sr.right > window.innerWidth) submenu.style.left = (parentRect.left - sr.width - 2) + 'px';
                        if (sr.bottom > window.innerHeight) submenu.style.top = (window.innerHeight - sr.height - 10) + 'px';
                        
                        setTimeout(function() {
                            document.addEventListener('click', function closeSub(ev) {
                                if (submenu && !submenu.contains(ev.target)) {
                                    submenu.remove(); submenu = null;
                                    document.removeEventListener('click', closeSub);
                                }
                            });
                        }, 100);
                    });
                };
            }
            
            function getEquationsWithSymbol(symbol, callback) {
                // Find equations containing this symbol by looking for .eqsym elements
                var equations = [];
                var eqSyms = document.querySelectorAll('.eqsym[data-sym="' + symbol + '"]');
                var equationIndices = new Set();
                
                // Determine the latest history index
                var allEqRows = document.querySelectorAll('.equation-row[id^="eq_"]');
                var maxHistIdx = 0;
                for (var j = 0; j < allEqRows.length; j++) {
                    var parts = allEqRows[j].id.split('_');
                    if (parts.length >= 2) maxHistIdx = Math.max(maxHistIdx, parseInt(parts[1]));
                }
                
                for (var i = 0; i < eqSyms.length; i++) {
                    var eqRow = findEquationRow(eqSyms[i]);
                    if (eqRow && eqRow.id) {
                        var idParts = eqRow.id.split('_');
                        if (idParts.length >= 3) {
                            var histIdx = parseInt(idParts[1]);
                            var eqIdx = parseInt(idParts[2]);
                            if (histIdx === maxHistIdx && !equationIndices.has(eqIdx)) {
                                equationIndices.add(eqIdx);
                                var eqText = eqRow.textContent || '';
                                eqText = eqText.trim().substring(0, 40);
                                if (eqText.length >= 40) eqText += '...';
                                equations.push({ index: eqIdx, display: eqText });
                            }
                        }
                    }
                }
                equations.sort(function(a, b) { return a.index - b.index; });
                callback(equations);
            }
            
            function createSeparator() {
                var sep = document.createElement('div');
                sep.className = 'equation-context-menu-separator';
                return sep;
            }
            
            function sendContextMenuCommand(command) {
                var instanceId = window._lastClickedInstanceId;
                if (instanceId) {
                    if (sendToBridge(instanceId, 1, command + '_' + Date.now())) {
                        console.log('Context menu command:', command);
                        return;
                    }
                }
                console.error('Could not send context menu command');
            }
        }
        </script>
        """
        display(HTML(js_code))
    
    def _on_symbol_clicked(self, change):
        """Handle symbol click from JavaScript."""
        if not change['new']:
            return
        
        # Parse the symbol name (remove timestamp)
        parts = change['new'].rsplit('_', 1)
        symbol_str = parts[0] if len(parts) > 1 else change['new']
        
        # Find the symbol object
        symbol = self._find_symbol(symbol_str)
        if symbol:
            self.selected_symbol = symbol
            self._update_display()
        
        # Reset the bridge
        self.click_bridge.value = ''
    
    def _on_context_menu_command(self, change):
        """Handle context menu command from JavaScript."""
        if not change['new']:
            return
        
        # Parse the command (remove timestamp)
        parts = change['new'].rsplit('_', 1)
        command = parts[0] if len(parts) > 1 else change['new']
        
        # Handle different commands
        if command == 'clear_selection':
            self.selected_symbol = None
            self._update_display()
        elif command.startswith('eliminate_auto:'):
            symbol_str = command.split(':', 1)[1]
            symbol = self._find_symbol(symbol_str)
            if symbol:
                self._eliminate_variable(symbol)
        elif command.startswith('eliminate_using:'):
            # Parse format: eliminate_using:symbol:eq_idx
            parts = command.split(':', 2)
            if len(parts) >= 2:
                symbol_str = parts[1]
                symbol = self._find_symbol(symbol_str)
                if symbol:
                    if len(parts) == 3:
                        # Specific equation index provided
                        eq_idx = int(parts[2])
                        _, current_eqs, _, _ = self.history[-1]
                        if eq_idx < len(current_eqs):
                            self._eliminate_using_equation(symbol, current_eqs[eq_idx])
                    else:
                        # Fallback: set dropdown (shouldn't happen with new menu)
                        self.eliminate_using_var_dropdown.value = symbol_str
        elif command.startswith('isolate_auto:'):
            symbol_str = command.split(':', 1)[1]
            symbol = self._find_symbol(symbol_str)
            if symbol:
                # Auto-select first equation with the symbol
                _, current_eqs, current_values, current_want = self.history[-1]
                equations_with_symbol = [
                    (idx, eq) for idx, eq in enumerate(current_eqs)
                    if eq != True and isinstance(eq, sp.Equality) and symbol in eq.free_symbols
                ]
                if len(equations_with_symbol) > 0:
                    idx, eq = equations_with_symbol[0]
                    self._isolate_variable(symbol, eq, idx)
        elif command.startswith('isolate:'):
            # Parse format: isolate:symbol:eq_idx (direct isolate for clicked equation)
            parts = command.split(':', 2)
            if len(parts) == 3:
                symbol_str = parts[1]
                eq_idx = int(parts[2])
                symbol = self._find_symbol(symbol_str)
                if symbol:
                    _, current_eqs, _, _ = self.history[-1]
                    if eq_idx < len(current_eqs):
                        self._isolate_variable(symbol, current_eqs[eq_idx], eq_idx)
        elif command.startswith('isolate_using:'):
            # Parse format: isolate_using:symbol:eq_idx
            parts = command.split(':', 2)
            if len(parts) >= 2:
                symbol_str = parts[1]
                symbol = self._find_symbol(symbol_str)
                if symbol:
                    if len(parts) == 3:
                        # Specific equation index provided
                        eq_idx = int(parts[2])
                        _, current_eqs, _, _ = self.history[-1]
                        if eq_idx < len(current_eqs):
                            self._isolate_variable(symbol, current_eqs[eq_idx], eq_idx)
        
        # Reset the bridge
        self.context_menu_bridge.value = ''
    
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
            source_eq_str = self._format_equation_short(source_equation, max_length=30)
            desc = f"Isolated {symbol} in Eq {eq_index+1} (was: {source_eq_str})"
            
            # Display new equations
            self.display_equations(new_eqs, current_values, current_want, desc)
            
        except ValueError as e:
            desc = f"Cannot isolate {symbol}: {str(e)}"
            self.history.append((desc, current_eqs, current_values, current_want))
            self._update_display()
        except Exception as e:
            desc = f"Error isolating {symbol}: {str(e)}"
            self.history.append((desc, current_eqs, current_values, current_want))
            self._update_display()
    
    def _inject_context_menu_css(self):
        """Inject CSS styles for the context menu."""
        css_code = """
        <style>
        .equation-context-menu {
            position: fixed;
            background: white;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
            z-index: 10000;
            min-width: 200px;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            font-size: 13px;
            padding: 4px 0;
        }
        
        .equation-context-menu-item {
            padding: 6px 16px;
            cursor: pointer;
            user-select: none;
            transition: background-color 0.1s;
        }
        
        .equation-context-menu-item:hover {
            background-color: #f0f0f0;
        }
        
        .equation-context-menu-item:active {
            background-color: #e0e0e0;
        }
        
        .equation-context-menu-separator {
            height: 1px;
            background-color: #e0e0e0;
            margin: 4px 0;
        }
        </style>
        """
        display(HTML(css_code))


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
