# MenuBar Component Specification

Provides desktop-like horizontal menu bars (File, Edit, Help) with vertical dropdown list overlay panels supporting alignment shift logic to prevent viewport boundary clipping.

## 1. Data Models

### `MenuItemSpec`
- `label`: string (top-level menu header)
- `children`: list of strings (dropdown items list, supporting `"-"` as separator line)

### `MenuBarSpec`
- `menus`: list of `MenuItemSpec` elements
- `selected_idx`: integer (focused top-level button)
- `active_menu_idx`: integer | null (index of open dropdown column, or None if dropdown closed)
- `selected_child_idx`: integer (focused dropdown sub-action)
- `spacing`: integer (character spacing between top menu headers)
- `menu_style`: string | null (theme token for normal top buttons)
- `selected_style`: string | null (theme token for active top button)
- `dropdown_style`: string | null (theme token for standard sub-actions)
- `dropdown_selected_style`: string | null (theme token for focused sub-actions)
- `width`: integer | null
- `height`: integer | null
- `spec_type`: `"menu_bar"`

---

## 2. Rendering & Boundary Alignment Math

Maintains structural dropdown alignment below the top header button. If the dropdown width exceeds the right viewport limit, it shifts column start coordinates left to keep the full overlay visible.

#### Pseudocode:
```
function render_menu_bar(spec: MenuBarSpec, max_width: int, max_height: int) -> list[str]:
    # 1. Render Top Header Bar (Line 0)
    top_parts = []
    offsets = []
    current_col = 0
    
    for idx, menu in enumerate(spec.menus):
        label = " " + menu.label + " "
        if idx > 0:
            top_parts.push(spacing_spaces)
            current_col += spacing
        offsets.push(current_col)
        top_parts.push(style_label(label, idx == spec.selected_idx))
        current_col += length(label)
        
    pad_len = max_width - raw_header_width
    lines = [join(top_parts) + pad_spaces(pad_len)]
    
    # 2. Render Dropdown Overlay Box
    if spec.active_menu_idx is not null:
        active = spec.menus[spec.active_menu_idx]
        inner_w = max_length(active.children)
        box_w = inner_w + 2
        start_col = offsets[spec.active_menu_idx]
        
        # Shift dropdown left if overflows right edge
        if start_col + box_w > max_width:
            start_col = max(0, max_width - box_w)
            
        box_lines = []
        box_lines.push("┌" + horizontal_line(inner_w) + "┐")
        for c_idx, child in enumerate(active.children):
            if child == "-":
                box_lines.push("├" + horizontal_line(inner_w) + "┤")
            else:
                padded = pad_right(child, inner_w)
                box_lines.push("│" + style_child(padded, c_idx == spec.selected_child_idx) + "│")
        box_lines.push("└" + horizontal_line(inner_w) + "┘")
        
        # Overlay rows onto output lines
        for r from 1 to max_height - 1:
            if r - 1 < length(box_lines):
                box_line = box_lines[r - 1]
                left = space(start_col)
                right = space(max(0, max_width - start_col - box_w))
                lines.push(left + box_line + right)
            else:
                lines.push(space(max_width))
                
    return lines[0:max_height]
```
