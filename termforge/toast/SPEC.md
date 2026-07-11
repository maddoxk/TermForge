# Toast Component Specification

Provides transient floating notification pop-ups stacked at designate viewport corners.

## 1. Data Models

### `ToastSpec`
- `text`: string (the notification message body)
- `toast_type`: string (`"success"`, `"info"`, `"warning"`, `"error"`)
- `duration_sec`: float (dismiss timer countdown threshold)
- `position`: string (`"top-left"`, `"top-right"`, `"bottom-left"`, `"bottom-right"`)
- `border_style`: string (`"single"`, `"double"`, `"rounded"`)
- `width`: integer | null
- `height`: integer | null
- `spec_type`: `"toast"`

---

## 2. Stacking & Positioning Math

Draws a `3`-row bordered box floating at corner boundaries. Computes vertical start rows and horizontal start columns inside `max_width` and `max_height` layout constraints.

#### Pseudocode:
```
function render_toast(spec: ToastSpec, max_width: int, max_height: int) -> list[str]:
    # Select border glyphs
    if spec.border_style == "rounded":
        tl, tr, bl, br, h, v = "╭", "╮", "╰", "╯", "─", "│"
    elif spec.border_style == "double":
        tl, tr, bl, br, h, v = "╔", "╗", "╚", "╝", "═", "║"
    else:
        tl, tr, bl, br, h, v = "┌", "┐", "└", "┘", "─", "│"
        
    prefix = "[" + uppercase(spec.toast_type) + "]"
    raw_content = prefix + " " + spec.text
    inner_w = length(raw_content)
    box_w = inner_w + 2
    box_h = 3
    
    # Calculate coordinate shifts
    if "right" in spec.position:
        start_x = max_width - box_w
    else:
        start_x = 0
    start_x = clamp(start_x, 0, max_width - box_w)
    
    if "bottom" in spec.position:
        start_y = max_height - box_h
    else:
        start_y = 0
    start_y = clamp(start_y, 0, max_height - box_h)
    
    # Style status prefix and borders
    top_line = style_border(tl + horizontal(inner_w) + tr)
    mid_line = style_border(v) + style_prefix(prefix) + " " + style_text(spec.text) + style_border(v)
    bot_line = style_border(bl + horizontal(inner_w) + br)
    box_lines = [top_line, mid_line, bot_line]
    
    # Overlay lines onto empty canvas lines
    lines = []
    for r from 0 to max_height - 1:
        if start_y <= r < start_y + box_h:
            box_idx = r - start_y
            lines.push(spaces(start_x) + box_lines[box_idx] + spaces(max_width - start_x - box_w))
        else:
            lines.push(spaces(max_width))
            
    return lines
```
---

## 3. Frame Tick Animation Scheduler Integration

For v1 animation integration, the framework ticks active notifications down:
```
function on_scheduler_tick(active_toasts: list[ToastInstance], delta_time: float):
    for toast in active_toasts:
        toast.remaining_duration -= delta_time
        if toast.remaining_duration <= 0:
            remove_from_stack(toast)
```
