# RadioButton Component Specification

Provides mutually exclusive option select button lists with customizable indicators and highlight overlays.

## 1. Data Models

### `RadioButtonItemSpec`
- `label`: string (the option label)
- `active`: boolean (whether this option is the active selection)

### `RadioButtonSpec`
- `items`: list of `RadioButtonItemSpec` options
- `selected_idx`: integer (focused keyboard cursor selection choice)
- `active_indicator`: string (active option indicator, default `"(●) "`)
- `inactive_indicator`: string (inactive option indicator, default `"( ) "`)
- `active_style`: string | null (theme style token for active selections)
- `selected_style`: string | null (theme style token for focused choice options)
- `inactive_style`: string | null (theme style token for standard inactive options)
- `width`: integer | null
- `height`: integer | null
- `spec_type`: `"radio_button"`

---

## 2. Rendering & Option Highlights Math

Iterates over radio option buttons, prefixing each with the active or inactive indicator prefix. Appends trailing spaces to match boundary layouts.

#### Pseudocode:
```
function render_radio_button(spec: RadioButtonSpec, max_width: int, max_height: int) -> list[str]:
    lines = []
    
    for idx, item in enumerate(spec.items):
        ind = spec.active_indicator if item.active else spec.inactive_indicator
        
        is_selected = (idx == spec.selected_idx)
        if is_selected:
            style = spec.selected_style
        else:
            style = spec.active_style if item.active else spec.inactive_style
            
        line = style_string(ind, style) + style_string(item.label, style)
        
        raw_len = length(ind) + length(item.label)
        if raw_len < max_width:
            line = line + spaces(max_width - raw_len)
            
        lines.push(line)
        
    while length(lines) < max_height:
        lines.push(spaces(max_width))
        
    return lines[0:max_height]
```
