# Combobox Component Specification

Provides dropdown selection boxes (comboboxes) that display floating option selections directly underneath closed inputs fields.

## 1. Data Models

### `ComboboxSpec`
- `options`: list of strings (raw choices stack)
- `selected_idx`: integer (index of selected option)
- `is_open`: boolean (whether dropdown choices panel is open)
- `active_hover_idx`: integer (focused item inside open dropdown choices panel)
- `caret`: string (dropdown indicator, default `"▼"`)
- `field_style`: string | null (theme style token for closed field box text)
- `dropdown_style`: string | null (theme style token for dropdown items)
- `hover_style`: string | null (theme style token for active focused item inside dropdown)
- `width`: integer | null
- `height`: integer | null
- `spec_type`: `"combobox"`

---

## 2. Rendering & Dropdown Overlays Math

Pads closed select fields using the longest option width. When open, overlays a bordered box directly below the select field containing options stacked, applying highlights to hover index positions.

#### Pseudocode:
```
function render_combobox(spec: ComboboxSpec, max_width: int, max_height: int) -> list[str]:
    # closed field line
    selected = spec.options[spec.selected_idx]
    max_opt_len = max_length(spec.options)
    padded_opt = pad_right(selected, max_opt_len)
    
    raw_field = "[ " + padded_opt + " ] " + spec.caret
    field_len = length(raw_field)
    
    lines = [style_string(raw_field, spec.field_style) + spaces(max_width - field_len)]
    
    if spec.is_open:
        inner_w = max_opt_len + 2
        box_w = inner_w + 2
        
        box_lines = []
        box_lines.push("┌" + horizontal(inner_w) + "┐")
        for idx, option in enumerate(spec.options):
            padded_opt = " " + pad_right(option, max_opt_len) + " "
            style = spec.hover_style if idx == spec.active_hover_idx else spec.dropdown_style
            box_lines.push("│" + style_string(padded_opt, style) + "│")
        box_lines.push("└" + horizontal(inner_w) + "┘")
        
        # Overlay lines
        for r from 1 to max_height - 1:
            box_idx = r - 1
            if box_idx < length(box_lines):
                lines.push(box_lines[box_idx] + spaces(max_width - box_w))
            else:
                lines.push(spaces(max_width))
    else:
        while length(lines) < max_height:
            lines.push(spaces(max_width))
            
    return lines[0:max_height]
```
