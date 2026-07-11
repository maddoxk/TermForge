# Tooltip Component Specification

Provides float help labels centered or anchored relative to specific layout coordinate indicators.

## 1. Data Models

### `TooltipSpec`
- `text`: string (the tooltip info string)
- `anchor_x`: integer (anchor column index, 0-indexed)
- `anchor_y`: integer (anchor row index, 0-indexed)
- `placement`: string (`"top"`, `"bottom"`, `"left"`, `"right"`)
- `bubble_style`: string | null (theme token for the border/bubble text)
- `pointer_style`: string | null (theme token for the pointer/arrow glyph)
- `width`: integer | null
- `height`: integer | null
- `spec_type`: `"tooltip"`

---

## 2. Rendering & Arrow Alignment Math

Calculates boundaries of a `3`-row bordered box positioned around the anchor coordinates. Incorporates direction pointers (`▲`, `▼`, `◀`, `▶`) pointing to the anchor coordinate.

#### Pseudocode:
```
function render_tooltip(spec: TooltipSpec, max_width: int, max_height: int) -> list[str]:
    inner_w = length(spec.text)
    box_w = inner_w + 2
    box_h = 3
    
    if spec.placement in ("top", "bottom"):
        start_x = spec.anchor_x - floor(inner_w / 2) - 1
        start_x = clamp(start_x, 0, max_width - box_w)
        ptr_idx = spec.anchor_x - start_x - 1
        ptr_idx = clamp(ptr_idx, 0, inner_w - 1)
        
        if spec.placement == "top":
            start_y = spec.anchor_y - 3
            top = "┌" + horizontal(inner_w) + "┐"
            mid = "│" + spec.text + "│"
            bot = "└" + horizontal(ptr_idx) + "▼" + horizontal(inner_w - 1 - ptr_idx) + "┘"
        else:
            start_y = spec.anchor_y + 1
            top = "┌" + horizontal(ptr_idx) + "▲" + horizontal(inner_w - 1 - ptr_idx) + "┐"
            mid = "│" + spec.text + "│"
            bot = "└" + horizontal(inner_w) + "┘"
            
    else:
        if spec.placement == "left":
            start_x = spec.anchor_x - box_w
            start_x = clamp(start_x, 0, max_width - box_w)
            start_y = spec.anchor_y - 1
            top = "┌" + horizontal(inner_w) + "┐"
            mid = "│" + spec.text + "▶"
            bot = "└" + horizontal(inner_w) + "┘"
        else:
            start_x = spec.anchor_x + 1
            start_x = clamp(start_x, 0, max_width - box_w)
            start_y = spec.anchor_y - 1
            top = "┌" + horizontal(inner_w) + "┐"
            mid = "◀" + spec.text + "│"
            bot = "└" + horizontal(inner_w) + "┘"
            
    start_y = clamp(start_y, 0, max_height - box_h)
    
    # Overlay lines onto empty canvas lines
    lines = []
    for r from 0 to max_height - 1:
        if start_y <= r < start_y + box_h:
            box_idx = r - start_y
            lines.push(spaces(start_x) + style_box(box_lines[box_idx]) + spaces(max_width - start_x - box_w))
        else:
            lines.push(spaces(max_width))
            
    return lines
```
