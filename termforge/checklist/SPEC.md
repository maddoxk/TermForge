# Checklist Component Specification

Provides toggleable multi-select option checklists with customizable checked/unchecked indicators and highlight overlays.

## 1. Data Models

### `ChecklistItemSpec`
- `label`: string (the option label)
- `checked`: boolean (checked indicator state)

### `ChecklistSpec`
- `items`: list of `ChecklistItemSpec` options
- `selected_idx`: integer (focused item index)
- `checked_indicator`: string (checkbox checked prefix, default `"[x] "`)
- `unchecked_indicator`: string (checkbox unchecked prefix, default `"[ ] "`)
- `checked_style`: string | null (theme token for checked options)
- `selected_style`: string | null (theme token for focused keyboard cursor option)
- `unchecked_style`: string | null (theme token for standard unchecked options)
- `width`: integer | null
- `height`: integer | null
- `spec_type`: `"checklist"`

---

## 2. Rendering & Option Highlights Math

Iterates over checklist items, prefixing each with the corresponding checked or unchecked indicator trail. Appends trailing spaces up to the layout width bounds.

#### Pseudocode:
```
function render_checklist(spec: ChecklistSpec, max_width: int, max_height: int) -> list[str]:
    lines = []
    
    for idx, item in enumerate(spec.items):
        ind = spec.checked_indicator if item.checked else spec.unchecked_indicator
        
        is_selected = (idx == spec.selected_idx)
        if is_selected:
            style = spec.selected_style
        else:
            style = spec.checked_style if item.checked else spec.unchecked_style
            
        line = style_string(ind, style) + style_string(item.label, style)
        
        raw_len = length(ind) + length(item.label)
        if raw_len < max_width:
            line = line + spaces(max_width - raw_len)
            
        lines.push(line)
        
    while length(lines) < max_height:
        lines.push(spaces(max_width))
        
    return lines[0:max_height]
```
