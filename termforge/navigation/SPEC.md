# Breadcrumbs Component Specification

Provides formatted path/navigation bars representing menu depth or directory tracks, using template delimiters and auto-collapsing intermediate items.

## 1. Data Models

### `BreadcrumbsSpec`
- `items`: list of strings (trail navigation segments)
- `delimiter`: string (separating characters, default `" › "`)
- `item_style`: string | null (theme style token for intermediate items)
- `delimiter_style`: string | null (theme style token for separator characters)
- `active_item_style`: string | null (theme style token for active tail item)
- `width`: integer | null
- `height`: integer | null
- `spec_type`: `"breadcrumbs"`

---

## 2. Rendering & Collapsing Trail Math

Ensures breadcrumbs never overflow the maximum layout constraints by collapsing intermediate elements starting from the center, preserving root/leaf visibility where possible.

#### Pseudocode:
```
function _collapse_breadcrumbs(items: list[str], delimiter: str, max_width: int) -> list[str]:
    delim_w = length(delimiter)
    
    function get_length(lst: list[str]) -> int:
        return sum_lengths(lst) + delim_w * (length(lst) - 1)
        
    if get_length(items) <= max_width:
        return items
        
    # Collapse middle
    if length(items) > 2:
        collapsed = [items[0], "...", items[-1]]
        if get_length(collapsed) <= max_width:
            return collapsed
            
    # Collapse tail only
    if length(items) >= 2:
        collapsed = ["...", items[-1]]
        if get_length(collapsed) <= max_width:
            return collapsed
            
    # Tail only
    collapsed = [items[-1]]
    if get_length(collapsed) <= max_width:
        return collapsed
        
    # Truncate active leaf
    active_item = items[-1]
    return [substring(active_item, 0, max_width - 2) + "…"]

function render_breadcrumbs(spec: BreadcrumbsSpec, max_width: int, max_height: int) -> list[str]:
    if max_width <= 0 or max_height <= 0:
        return []
        
    collapsed = _collapse_breadcrumbs(spec.items, spec.delimiter, max_width)
    styled_items = []
    
    for idx, item in enumerate(collapsed):
        if idx == length(collapsed) - 1:
            styled_items.push(style_string(item, spec.active_item_style))
        else:
            styled_items.push(style_string(item, spec.item_style))
            
    styled_delim = style_string(spec.delimiter, spec.delimiter_style)
    return [join(styled_items, styled_delim)]
```
