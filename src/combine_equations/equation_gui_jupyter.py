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

__version__ = "1.2.1"

import ipywidgets as widgets
from IPython.display import display, HTML, Markdown
import sympy as sp
from typing import List, Dict, Any, Optional, Tuple
import html


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
        # Get all symbols in the equation
        all_symbols = sorted(eq.free_symbols, key=lambda s: str(s))
        
        # Build colored LaTeX with clickable symbols
        lhs_colored = self._colorize_latex(eq.lhs, values, want, all_symbols, clickable=True)
        rhs_colored = self._colorize_latex(eq.rhs, values, want, all_symbols, clickable=True)
        
        # Create equation display with unique ID
        eq_id = f"eq_{history_idx}_{eq_idx}"
        eq_html = f"""
        <div id="{eq_id}" style='margin: 8px 0; padding: 10px; background: white; border-left: 3px solid #4CAF50;'>
            <div style='font-size: 18px; font-family: "Computer Modern", "Times New Roman", serif;'>
                {lhs_colored} = {rhs_colored}
            </div>
        </div>
        """
        
        display(HTML(eq_html))
    
    def _colorize_latex(self, expr, values, want, all_symbols, clickable=False) -> str:
        """Convert expression to LaTeX with color highlighting for symbols."""
        import json
        latex = sp.latex(expr)
        
        # Sort symbols by length (longest first) to avoid partial replacements
        sorted_symbols = sorted(all_symbols, key=lambda s: len(sp.latex(s)), reverse=True)
        
        # Build a map of symbol to its replacement
        symbol_map = {}
        # Build a map of LaTeX to symbol name for JavaScript
        latex_to_symbol = {}
        
        # For each symbol, colorize it
        for symbol in sorted_symbols:
            symbol_str = str(symbol)
            symbol_latex = sp.latex(symbol)
            
            if symbol_latex not in latex:
                continue
            
            # Store mapping for JavaScript
            latex_to_symbol[symbol_latex] = symbol_str
            
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
                colored_latex = f'\\bbox[yellow,2pt]{{\\color{{{self._color_to_latex(color)}}}{{{symbol_latex}}}}}'
            else:
                colored_latex = f'\\color{{{self._color_to_latex(color)}}}{{{symbol_latex}}}'
            
            symbol_map[symbol_latex] = (colored_latex, symbol_str)
        
        # Replace symbols in LaTeX
        for symbol_latex, (colored_latex, symbol_str) in symbol_map.items():
            latex = latex.replace(symbol_latex, colored_latex)
        
        # Wrap in LaTeX delimiters
        latex_html = f"\\({latex}\\)"
        
        # If clickable, wrap the entire expression in a clickable span with data attribute
        if clickable:
            # Create a wrapper with symbol mapping for accurate click detection
            symbol_mapping_json = json.dumps(latex_to_symbol).replace('"', '&quot;')
            result = f"""<span class="equation-expr clickable-symbol" style="cursor: pointer; display: inline-block;" 
                           data-symbol-map="{symbol_mapping_json}"
                           data-instance-id="{self.instance_id}">{latex_html}</span>"""
        else:
            result = f"<span>{latex_html}</span>"
        
        return result
    
    def _color_to_latex(self, hex_color: str) -> str:
        """Convert hex color to LaTeX color name."""
        color_map = {
            '#CC0000': 'red',
            '#00AA00': 'green',
            'black': 'black'
        }
        return color_map.get(hex_color, 'black')
    
    def _make_clickable_wrapper(self, latex_html: str, all_symbols) -> str:
        """Wrap LaTeX HTML with clickable functionality."""
        # Extract all symbol strings for the data attribute
        symbol_strs = [str(s) for s in all_symbols]
        symbols_json = ','.join(symbol_strs)
        
        # Wrap in a span with click handler
        wrapper = f"""
        <span class="clickable-equation" data-symbols="{symbols_json}" 
              style="cursor: pointer; user-select: none; display: inline-block; 
                     padding: 2px; border-radius: 3px; transition: background-color 0.2s;" 
              onmouseover="this.style.backgroundColor='#f0f0f0'" 
              onmouseout="this.style.backgroundColor='transparent'"
              onclick="handleEquationClick(event, this)"
              title="Click to highlight symbols in this expression">
            {latex_html}
        </span>
        """
        return wrapper
    
    def _inject_javascript(self):
        """Inject JavaScript for handling symbol clicks and context menu using event delegation."""
        
        # First inject CSS for context menu
        self._inject_context_menu_css()
        
        js_code = """
        <script>
        // Only add listener once - check if already added
        if (!window._equationGuiListenerAdded) {
            window._equationGuiListenerAdded = true;
            
            // Context menu state
            window._activeContextMenu = null;
            
            // Use event delegation - attach listener to document
            document.addEventListener('click', function(event) {
                // Close context menu on any click
                if (window._activeContextMenu) {
                    window._activeContextMenu.remove();
                    window._activeContextMenu = null;
                }
                // Find the clicked element or its parent with the clickable-symbol class
                var element = event.target;
                var wrapper = null;
                
                // Walk up to find the span with data-symbol-map (increased depth for MathJax fractions)
                for (var i = 0; i < 20 && element; i++) {
                    if (element.classList && element.classList.contains('clickable-symbol')) {
                        wrapper = element;
                        break;
                    }
                    element = element.parentElement;
                }
                
                if (!wrapper) {
                    // Debug: check if this was in an equation area
                    var checkEl = event.target;
                    for (var i = 0; i < 20 && checkEl; i++) {
                        if (checkEl.classList && checkEl.classList.contains('equation-expr')) {
                            console.log('Found equation-expr but not clickable-symbol at level', i);
                            console.log('Element:', checkEl);
                            break;
                        }
                        checkEl = checkEl.parentElement;
                    }
                    return; // Not a symbol click
                }
            
            // Get symbol mapping from element's data attribute
            var symbolMapStr = wrapper.getAttribute('data-symbol-map');
            if (!symbolMapStr) {
                console.error('No symbol mapping found');
                return;
            }
            
            var symbolMap = JSON.parse(symbolMapStr);
            
            // Try to get text from the clicked target first (more specific)
            // For fractions, we want to identify if we're in numerator or denominator
            var target = event.target;
            var clickedText = '';
            var foundMatch = false;
            
            // Walk up from target, trying to find the smallest element with matching symbols
            var testElement = target;
            for (var j = 0; j < 15 && testElement && testElement !== wrapper; j++) {
                var text = testElement.textContent || testElement.innerText;
                if (text && text.trim().length >= 2) {
                    var testClean = text.trim().replace(/[\\s\\u2212+*/=()\\[\\]\\-]/g, '');
                    // Check if this text contains any symbol
                    for (var key in symbolMap) {
                        var cleanPattern = key.replace(/[_{}\\s]/g, '');
                        if (testClean.includes(cleanPattern)) {
                            clickedText = text.trim();
                            foundMatch = true;
                            break;
                        }
                    }
                    if (foundMatch) break;
                }
                testElement = testElement.parentElement;
            }
            
            // Fallback to wrapper if no match found
            if (!clickedText || !clickedText.trim()) {
                clickedText = wrapper.textContent || wrapper.innerText;
            }
            
            if (!clickedText || !clickedText.trim()) {
                console.log('No text found in clicked element');
                return;
            }
            
            clickedText = clickedText.trim();
            console.log('Clicked text:', clickedText);
            
            // Find all matching symbols
            var cleanText = clickedText.replace(/[\\s\\u2212+*/=()\\[\\]\\-]/g, '');
            var matches = [];
            
            for (var key in symbolMap) {
                var cleanPattern = key.replace(/[_{}\\s]/g, '');
                if (cleanText.includes(cleanPattern)) {
                    matches.push({
                        latex: key,
                        symbol: symbolMap[key],
                        pattern: cleanPattern,
                        index: cleanText.indexOf(cleanPattern)
                    });
                }
            }
            
            var symbolStr = null;
            
            if (matches.length === 0) {
                // No matches - use first symbol as fallback
                var keys = Object.keys(symbolMap);
                symbolStr = symbolMap[keys[0]];
                console.log('No match found, using fallback:', symbolStr);
            } else if (matches.length === 1) {
                // Single match - use it
                symbolStr = matches[0].symbol;
            } else {
                // Multiple matches - use X position (and Y for fractions)
                matches.sort(function(a, b) { return a.index - b.index; });
                
                var rect = wrapper.getBoundingClientRect();
                var clickX = event.clientX - rect.left;
                var clickY = event.clientY - rect.top;
                var clickRatioX = clickX / rect.width;
                var clickRatioY = clickY / rect.height;
                
                var textLen = cleanText.length;
                var filtered = matches;
                
                // Get the LaTeX source from the wrapper's innerHTML to check for fractions
                var wrapperHTML = wrapper.innerHTML || '';
                var hasFraction = wrapperHTML.indexOf('frac') !== -1;
                
                if (hasFraction) {
                    // Use Y position to filter to numerator or denominator group
                    // If Y < 0.5, keep symbols in first half of text (numerator)
                    // If Y >= 0.5, keep symbols in second half of text (denominator)
                    var midIndex = textLen / 2;
                    filtered = matches.filter(function(m) {
                        var isInFirstHalf = (m.index + m.pattern.length / 2) < midIndex;
                        return clickRatioY < 0.5 ? isInFirstHalf : !isInFirstHalf;
                    });
                    
                    // If filter removed everything, use all matches
                    if (filtered.length === 0) {
                        filtered = matches;
                    }
                    
                    console.log('Y filter (fraction): clickY=' + clickRatioY.toFixed(2) + ', filtered to:', filtered.map(function(m) { return m.symbol; }));
                } else {
                    console.log('No fraction - using X position only');
                }
                
                // Step 2: Within filtered group, use X position
                var bestMatch = filtered[0];
                
                if (filtered.length > 1) {
                    // Find the visual positions of filtered symbols relative to each other
                    var minIdx = filtered[0].index;
                    var maxIdx = filtered[filtered.length - 1].index + filtered[filtered.length - 1].pattern.length;
                    var span = maxIdx - minIdx;
                    
                    var bestDist = 999;
                    for (var mi = 0; mi < filtered.length; mi++) {
                        var m = filtered[mi];
                        // Position within the filtered group (0 to 1)
                        var relPos = span > 0 ? (m.index - minIdx + m.pattern.length / 2) / span : 0.5;
                        var dist = Math.abs(relPos - clickRatioX);
                        if (dist < bestDist) {
                            bestDist = dist;
                            bestMatch = m;
                        }
                    }
                }
                
                symbolStr = bestMatch.symbol;
                console.log('Final pick: clickX=' + clickRatioX.toFixed(2) + ', picked:', symbolStr);
                console.log('All matches:', matches.map(function(m) { return m.symbol + '@' + m.index; }));
            }
            
            if (!symbolStr) {
                console.log('No symbol found');
                return;
            }
            
            var newValue = symbolStr + '_' + Date.now();
            
            // Get the instance ID from the clicked element
            var instanceId = wrapper.getAttribute('data-instance-id');
            
            // Find the container for this instance
            var container = null;
            if (instanceId) {
                var elem = wrapper;
                for (var k = 0; k < 20 && elem; k++) {
                    if (elem.classList && elem.classList.contains('eqgui-instance-' + instanceId)) {
                        container = elem;
                        break;
                    }
                    elem = elem.parentElement;
                }
            }
            
            // Find the hidden text widget within this container
            if (container) {
                var inputs = container.querySelectorAll('input[type="text"]');
                var hiddenInputs = [];
                for (var i = 0; i < inputs.length; i++) {
                    var input = inputs[i];
                    var parent = input.parentElement;
                    if (parent && parent.style && parent.style.display === 'none') {
                        hiddenInputs.push(input);
                    }
                }
                
                // First hidden input should be click bridge
                if (hiddenInputs.length > 0) {
                    var input = hiddenInputs[0];
                    input.value = newValue;
                    
                    // Trigger events to notify ipywidgets
                    var inputEvent = new Event('input', { bubbles: true });
                    var changeEvent = new Event('change', { bubbles: true });
                    input.dispatchEvent(inputEvent);
                    input.dispatchEvent(changeEvent);
                    
                    console.log('Symbol click registered:', symbolStr, 'for instance:', instanceId);
                    return; // Success!
                }
                console.error('Could not find click bridge in container for instance:', instanceId);
                return;
            }
            
            // Fallback: old method for backward compatibility
            var searchRoot = wrapper;
            for (var k = 0; k < 10; k++) {
                searchRoot = searchRoot.parentElement;
                if (!searchRoot) break;
                
                // Look for the hidden input in this container
                var inputs = searchRoot.querySelectorAll('input[type="text"]');
                for (var m = 0; m < inputs.length; m++) {
                    var input = inputs[m];
                    // Check if this is a hidden widget
                    var parent = input.parentElement;
                    if (parent && parent.style && parent.style.display === 'none') {
                        // Found it! Update the value
                        input.value = newValue;
                        
                        // Trigger events to notify ipywidgets
                        var inputEvent = new Event('input', { bubbles: true });
                        var changeEvent = new Event('change', { bubbles: true });
                        input.dispatchEvent(inputEvent);
                        input.dispatchEvent(changeEvent);
                        
                        console.log('Symbol click registered:', symbolStr);
                        return; // Success!
                    }
                }
            }
            console.error('Could not find hidden widget');
        });
        
        // Right-click handler for context menu (use capture phase for better control)
        document.addEventListener('contextmenu', function(event) {
            // Find the clicked element or its parent with the clickable-symbol class
            var element = event.target;
            var wrapper = null;
            
            // Walk up to find the span with data-symbol-map
            for (var i = 0; i < 20 && element; i++) {
                if (element.classList && element.classList.contains('clickable-symbol')) {
                    wrapper = element;
                    break;
                }
                element = element.parentElement;
            }
            
            if (!wrapper) {
                return true; // Not a symbol - allow default context menu
            }
            
            // Prevent default browser context menu
            event.preventDefault();
            event.stopPropagation();
            event.stopImmediatePropagation();
            
            // Get symbol from click (reuse existing logic)
            var symbolMapStr = wrapper.getAttribute('data-symbol-map');
            if (!symbolMapStr) {
                return;
            }
            
            var symbolMap = JSON.parse(symbolMapStr);
            var target = event.target;
            var clickedText = '';
            var foundMatch = false;
            
            // Find clicked text
            var testElement = target;
            for (var j = 0; j < 15 && testElement && testElement !== wrapper; j++) {
                var text = testElement.textContent || testElement.innerText;
                if (text && text.trim().length >= 2) {
                    var testClean = text.trim().replace(/[\\s\\u2212+*/=()\\[\\]\\-]/g, '');
                    for (var key in symbolMap) {
                        var cleanPattern = key.replace(/[_{}\\s]/g, '');
                        if (testClean.includes(cleanPattern)) {
                            clickedText = text.trim();
                            foundMatch = true;
                            break;
                        }
                    }
                    if (foundMatch) break;
                }
                testElement = testElement.parentElement;
            }
            
            if (!clickedText || !clickedText.trim()) {
                clickedText = wrapper.textContent || wrapper.innerText;
            }
            
            if (!clickedText || !clickedText.trim()) {
                return;
            }
            
            clickedText = clickedText.trim();
            
            // Find matching symbols
            var cleanText = clickedText.replace(/[\\s\\u2212+*/=()\\[\\]\\-]/g, '');
            var matches = [];
            
            for (var key in symbolMap) {
                var cleanPattern = key.replace(/[_{}\\s]/g, '');
                if (cleanText.includes(cleanPattern)) {
                    matches.push({
                        latex: key,
                        symbol: symbolMap[key],
                        pattern: cleanPattern,
                        index: cleanText.indexOf(cleanPattern)
                    });
                }
            }
            
            var symbolStr = null;
            
            if (matches.length === 0) {
                var keys = Object.keys(symbolMap);
                symbolStr = symbolMap[keys[0]];
            } else if (matches.length === 1) {
                symbolStr = matches[0].symbol;
            } else {
                // Use position-based selection (similar to click handler)
                matches.sort(function(a, b) { return a.index - b.index; });
                var rect = wrapper.getBoundingClientRect();
                var clickX = event.clientX - rect.left;
                var clickRatioX = clickX / rect.width;
                symbolStr = matches[0].symbol;
                
                var bestDist = 999;
                for (var mi = 0; mi < matches.length; mi++) {
                    var m = matches[mi];
                    var relPos = m.index / cleanText.length;
                    var dist = Math.abs(relPos - clickRatioX);
                    if (dist < bestDist) {
                        bestDist = dist;
                        symbolStr = m.symbol;
                    }
                }
            }
            
            if (!symbolStr) {
                event.preventDefault();
                return false;
            }
            
            // Get the equation index from the clicked element
            var eqIdx = null;
            var eqDiv = wrapper.closest('[id^="eq_"]');
            if (eqDiv) {
                var idParts = eqDiv.id.split('_');
                if (idParts.length >= 3) {
                    eqIdx = parseInt(idParts[2]);
                }
            }
            
            // Store instance ID globally for context menu commands
            var instanceId = wrapper.getAttribute('data-instance-id');
            if (instanceId) {
                window._lastClickedInstanceId = instanceId;
            }
            
            // Show context menu
            showContextMenu(event.clientX, event.clientY, symbolStr, eqIdx);
            
            // Return false to prevent any other handlers
            return false;
        }, true); // Use capture phase for better event control
        
        // Function to show context menu
        function showContextMenu(x, y, symbol, eqIdx) {
            // Close any existing menu
            if (window._activeContextMenu) {
                window._activeContextMenu.remove();
            }
            
            // Create menu container
            var menu = document.createElement('div');
            menu.className = 'equation-context-menu';
            menu.style.left = x + 'px';
            menu.style.top = y + 'px';
            
            // Prevent context menu on the menu itself
            menu.oncontextmenu = function(e) {
                e.preventDefault();
                e.stopPropagation();
                return false;
            };
            
            // Add menu items
            addMenuItem(menu, "Eliminate '" + symbol + "' (auto)", 'eliminate_auto:' + symbol, false);
            addMenuItemWithSubmenu(menu, "Eliminate '" + symbol + "' using...", symbol, x, y, 'eliminate');
            menu.appendChild(createSeparator());
            
            // If we know which equation was clicked, show direct "Isolate" option
            if (eqIdx !== null) {
                addMenuItem(menu, "Isolate '" + symbol + "'", 'isolate:' + symbol + ':' + eqIdx, false);
            }
            addMenuItemWithSubmenu(menu, "Isolate '" + symbol + "' in...", symbol, x, y, 'isolate');
            menu.appendChild(createSeparator());
            addMenuItem(menu, "Clear selection", 'clear_selection', false);
            
            // Prevent menu from going off-screen
            document.body.appendChild(menu);
            
            var menuRect = menu.getBoundingClientRect();
            if (menuRect.right > window.innerWidth) {
                menu.style.left = (x - menuRect.width) + 'px';
            }
            if (menuRect.bottom > window.innerHeight) {
                menu.style.top = (y - menuRect.height) + 'px';
            }
            
            window._activeContextMenu = menu;
        }
        
        function addMenuItem(menu, label, command, hasSubmenu) {
            var item = document.createElement('div');
            item.className = 'equation-context-menu-item';
            
            if (hasSubmenu) {
                // Add arrow indicator for submenu
                item.innerHTML = label + ' <span style="float: right; margin-left: 20px;">▶</span>';
            } else {
                item.textContent = label;
            }
            
            if (!hasSubmenu) {
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
            
            // Show submenu on click
            item.onclick = function(e) {
                e.stopPropagation();
                
                // Close existing submenu if any
                if (submenu) {
                    submenu.remove();
                    submenu = null;
                    return;
                }
                
                // Get equations with this symbol from Python side
                // We'll request them via a special command
                getEquationsWithSymbol(symbol, function(equations) {
                    if (equations.length === 0) {
                        return;
                    }
                    
                    // Create submenu
                    submenu = document.createElement('div');
                    submenu.className = 'equation-context-menu';
                    
                    // Position submenu to the right of parent item
                    var itemRect = item.getBoundingClientRect();
                    var parentRect = parentMenu.getBoundingClientRect();
                    submenu.style.left = (parentRect.right + 2) + 'px';
                    submenu.style.top = itemRect.top + 'px';
                    
                    // Add equation options
                    for (var i = 0; i < equations.length; i++) {
                        var eq = equations[i];
                        var command = action + '_using:' + symbol + ':' + eq.index;
                        // Create submenu item with custom handler that closes both menus
                        var submenuItem = document.createElement('div');
                        submenuItem.className = 'equation-context-menu-item';
                        submenuItem.textContent = 'Eq ' + (eq.index + 1) + ': ' + eq.display;
                        (function(cmd) {
                            submenuItem.onclick = function(e) {
                                e.stopPropagation();
                                sendContextMenuCommand(cmd);
                                // Close submenu
                                if (submenu) {
                                    submenu.remove();
                                    submenu = null;
                                }
                                // Close parent menu
                                if (parentMenu) {
                                    parentMenu.remove();
                                }
                                window._activeContextMenu = null;
                            };
                        })(command);
                        submenu.appendChild(submenuItem);
                    }
                    
                    document.body.appendChild(submenu);
                    
                    // Adjust if off-screen
                    var submenuRect = submenu.getBoundingClientRect();
                    if (submenuRect.right > window.innerWidth) {
                        submenu.style.left = (parentRect.left - submenuRect.width - 2) + 'px';
                    }
                    if (submenuRect.bottom > window.innerHeight) {
                        submenu.style.top = (window.innerHeight - submenuRect.height - 10) + 'px';
                    }
                    
                    // Close submenu when clicking outside
                    setTimeout(function() {
                        document.addEventListener('click', function closeSubmenu(e) {
                            if (submenu && !submenu.contains(e.target)) {
                                submenu.remove();
                                submenu = null;
                                document.removeEventListener('click', closeSubmenu);
                            }
                        });
                    }, 100);
                });
            };
        }
        
        function getEquationsWithSymbol(symbol, callback) {
            // For now, we'll extract equations directly from the DOM
            // Look for equation displays in the current view
            var equations = [];
            
            // Find all clickable symbols with this symbol's data
            var clickableSymbols = document.querySelectorAll('.clickable-symbol');
            var equationIndices = new Set();
            
            for (var i = 0; i < clickableSymbols.length; i++) {
                var elem = clickableSymbols[i];
                var symbolMapStr = elem.getAttribute('data-symbol-map');
                if (symbolMapStr) {
                    try {
                        var symbolMap = JSON.parse(symbolMapStr);
                        // Check if this element contains our symbol
                        for (var key in symbolMap) {
                            if (symbolMap[key] === symbol) {
                                // Extract equation index from parent structure
                                var eqDiv = elem.closest('[id^="eq_"]');
                                if (eqDiv) {
                                    var idParts = eqDiv.id.split('_');
                                    if (idParts.length >= 3) {
                                        var histIdx = parseInt(idParts[1]);
                                        var eqIdx = parseInt(idParts[2]);
                                        // Only include equations from the latest history item
                                        var allEqDivs = document.querySelectorAll('[id^="eq_"]');
                                        var maxHistIdx = 0;
                                        for (var j = 0; j < allEqDivs.length; j++) {
                                            var parts = allEqDivs[j].id.split('_');
                                            if (parts.length >= 2) {
                                                maxHistIdx = Math.max(maxHistIdx, parseInt(parts[1]));
                                            }
                                        }
                                        if (histIdx === maxHistIdx && !equationIndices.has(eqIdx)) {
                                            equationIndices.add(eqIdx);
                                            // Get equation text for display
                                            var eqText = eqDiv.textContent || '';
                                            eqText = eqText.trim().substring(0, 40);
                                            if (eqText.length >= 40) eqText += '...';
                                            equations.push({
                                                index: eqIdx,
                                                display: eqText
                                            });
                                        }
                                    }
                                }
                                break;
                            }
                        }
                    } catch(e) {}
                }
            }
            
            // Sort by index
            equations.sort(function(a, b) { return a.index - b.index; });
            callback(equations);
        }
        
        function createSeparator() {
            var sep = document.createElement('div');
            sep.className = 'equation-context-menu-separator';
            return sep;
        }
        
        function sendContextMenuCommand(command) {
            // Get instance ID from the last clicked element (stored globally)
            var instanceId = window._lastClickedInstanceId;
            
            if (instanceId) {
                // Find the container for this instance
                var containers = document.querySelectorAll('.eqgui-instance-' + instanceId);
                if (containers.length > 0) {
                    var container = containers[0];
                    var inputs = container.querySelectorAll('input[type="text"]');
                    var hiddenInputs = [];
                    for (var i = 0; i < inputs.length; i++) {
                        var input = inputs[i];
                        var parent = input.parentElement;
                        if (parent && parent.style && parent.style.display === 'none') {
                            hiddenInputs.push(input);
                        }
                    }
                    
                    // Second hidden input should be context menu bridge
                    if (hiddenInputs.length >= 2) {
                        var input = hiddenInputs[1];
                        var testValue = command + '_' + Date.now();
                        input.value = testValue;
                        
                        var inputEvent = new Event('input', { bubbles: true });
                        var changeEvent = new Event('change', { bubbles: true });
                        input.dispatchEvent(inputEvent);
                        input.dispatchEvent(changeEvent);
                        
                        console.log('Context menu command sent:', command, 'for instance:', instanceId);
                        return;
                    }
                    console.error('Could not find context menu bridge in container for instance:', instanceId);
                    return;
                }
                console.error('Could not find container for instance:', instanceId);
            }
            
            // Fallback: Find the hidden context menu widget using old method
            // Look for hidden text inputs and try to find the second one (context menu bridge)
            var inputs = document.querySelectorAll('input[type="text"]');
            var hiddenInputs = [];
            
            for (var i = 0; i < inputs.length; i++) {
                var input = inputs[i];
                var parent = input.parentElement;
                if (parent && parent.style && parent.style.display === 'none') {
                    hiddenInputs.push(input);
                }
            }
            
            // We need at least 2 hidden inputs (click_bridge and context_menu_bridge)
            // The context_menu_bridge should be the second one (or we can try both)
            if (hiddenInputs.length >= 2) {
                // Try the second hidden input (context menu bridge)
                var input = hiddenInputs[1];
                var testValue = command + '_' + Date.now();
                input.value = testValue;
                
                var inputEvent = new Event('input', { bubbles: true });
                var changeEvent = new Event('change', { bubbles: true });
                input.dispatchEvent(inputEvent);
                input.dispatchEvent(changeEvent);
                
                console.log('Context menu command sent:', command);
                return;
            } else if (hiddenInputs.length === 1) {
                // Fallback: only one hidden input, try it anyway
                var input = hiddenInputs[0];
                var testValue = command + '_' + Date.now();
                input.value = testValue;
                
                var inputEvent = new Event('input', { bubbles: true });
                var changeEvent = new Event('change', { bubbles: true });
                input.dispatchEvent(inputEvent);
                input.dispatchEvent(changeEvent);
                
                console.log('Context menu command sent to single bridge:', command);
                return;
            }
            
            console.error('Could not find context menu bridge widget. Found', hiddenInputs.length, 'hidden inputs');
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
