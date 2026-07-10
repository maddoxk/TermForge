# TermForge Windows Module Specification

This module defines windows, split-pane containers, z-ordering, focus state highlight, and scrolling.

## 1. Data Structures

### `WindowSpec`
- `title`: string
- `border_style`: `BorderStyle`
- `width`: integer | null
- `height`: integer | null
- `scroll_y`: integer
- `focused`: boolean
- `z_index`: integer
- `content`: `RenderableSpec` | null

### `PaneSpec`
A split container layout.
- `direction`: `FlexDirection` (ROW or COLUMN)
- `children`: list of `RenderableSpec`
- `ratios`: list of floats | null
- `gap`: integer

### `ModalSpec`
- `content`: `RenderableSpec` | null
- `backdrop`: boolean
- `width`: integer
- `height`: integer

---

## 2. Algorithms

### Pane Size Composition (`compose_panes`)
Splits an available screen area into multiple box-regions according to the pane direction and ratio weights.

#### Pseudocode:
```
function compose_panes(spec: PaneSpec, available: Size) -> list[tuple[Position, Size, RenderableSpec]]:
    num_children = length(spec.children)
    ratios = spec.ratios if spec.ratios is not null else list_of_ones(num_children)
    total_ratio = sum(ratios)
    gaps_space = spec.gap * (num_children - 1)
    
    results = []
    
    if spec.direction == ROW:
        rem_w = max(0, available.width - gaps_space)
        curr_x = 0
        for i = 0 to num_children - 1:
            w = (ratios[i] / total_ratio) * rem_w
            if i == num_children - 1:
                w = available.width - curr_x
            child_size = Size(w, available.height)
            child_pos = Position(curr_x, 0)
            results.push((child_pos, child_size, spec.children[i]))
            curr_x = curr_x + w + spec.gap
    else: # COLUMN
        rem_h = max(0, available.height - gaps_space)
        curr_y = 0
        for i = 0 to num_children - 1:
            h = (ratios[i] / total_ratio) * rem_h
            if i == num_children - 1:
                h = available.height - curr_y
            child_size = Size(available.width, h)
            child_pos = Position(0, curr_y)
            results.push((child_pos, child_size, spec.children[i]))
            curr_y = curr_y + h + spec.gap
            
    return results
```

### Scrolling (`apply_scroll`)
Extracts a window's viewport lines starting from the scroll offset.

#### Pseudocode:
```
function apply_scroll(lines: list[string], scroll_y: int, viewport_height: int) -> list[string]:
    if length(lines) <= viewport_height:
        return pad_lines_with_empty(lines, viewport_height)
    max_scroll = length(lines) - viewport_height
    start = max(0, min(scroll_y, max_scroll))
    return lines[start : start + viewport_height]
```
