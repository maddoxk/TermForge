# Accordion Component Specification

Provides vertical collapse/expand details panels displaying text blocks indented under caret-prefixed header section titles.

## 1. Data Models

### `AccordionItemSpec`
- `title`: string (section title)
- `details`: string (multiline details text visible when expanded)
- `is_expanded`: boolean (expanded state toggle)

### `AccordionSpec`
- `items`: list of `AccordionItemSpec` options
- `selected_idx`: integer (focused keyboard cursor selection index)
- `collapsed_caret`: string (collapsed toggle indicator prefix, default `"> "`)
- `expanded_caret`: string (expanded toggle indicator prefix, default `"v "`)
- `active_style`: string | null (theme style token for expanded header items)
- `selected_style`: string | null (theme style token for focused option choice)
- `inactive_style`: string | null (theme style token for collapsed normal items)
- `details_style`: string | null (theme style token for expanded details descriptions)
- `width`: integer | null
- `height`: integer | null
- `spec_type`: `"accordion"`

---

## 2. Collapse/Expand Formatting & Indentation Math

Iterates over accordion items, prefixing each header with the collapsed or expanded caret. If expanded, indents content details block lines by 4 spaces (`"    "`). Pads layout lines to match exact boundaries.

#### Pseudocode:
```
function render_accordion(spec: AccordionSpec, max_width: int, max_height: int) -> list[str]:
    lines = []
    
    for idx, item in enumerate(spec.items):
        caret = if item.is_expanded then spec.expanded_caret else spec.collapsed_caret
        
        is_selected = (idx == spec.selected_idx)
        if is_selected:
            style = spec.selected_style
        else:
            style = spec.active_style if item.is_expanded else spec.inactive_style
            
        hdr = caret + item.title
        lines.push(style_string(hdr, style) + spaces(max_width - length(hdr)))
        
        if item.is_expanded and item.details is not empty:
            det_lines = split(item.details, "\n")
            for det in det_lines:
                raw_det = "    " + det
                lines.push(style_string(raw_det, spec.details_style) + spaces(max_width - length(raw_det)))
                
    while length(lines) < max_height:
        lines.push(spaces(max_width))
        
    return lines[0:max_height]
```
