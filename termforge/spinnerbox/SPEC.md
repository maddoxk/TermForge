# SpinnerBox Component Specification

Provides horizontal spinner widgets for decrementing/incrementing numeric values.

## 1. Data Models

### `SpinnerBoxSpec`
- `value`: integer (current value)
- `min_val`: integer | null (minimum value boundary limit)
- `max_val`: integer | null (maximum value boundary limit)
- `step`: integer (increment/decrement step size)
- `label`: string (description text next to spinner)
- `left_caret`: string (decrement caret character, default `"◀"`)
- `right_caret`: string (increment caret character, default `"▶"`)
- `caret_style`: string | null (theme style token for carets)
- `value_style`: string | null (theme style token for number value text)
- `label_style`: string | null (theme style token for description label)
- `width`: integer | null
- `height`: integer | null
- `spec_type`: `"spinner_box"`

---

## 2. Horizontal Layout Spacing Math

Renders a spinner widget block of constant size wrapping the formatted value. Separates description labels and spinner widget blocks with spaces to align flush right.

#### Pseudocode:
```
function render_spinner_box(spec: SpinnerBoxSpec, max_width: int, max_height: int) -> list[str]:
    # value padding length
    if spec.min_val is not null and spec.max_val is not null:
        max_val_len = max(length(string(spec.min_val)), length(string(spec.max_val)))
    else:
        max_val_len = 3
        
    padded_val = center_string(string(spec.value), max_val_len)
    
    styled_left = style_string(spec.left_caret, spec.caret_style)
    styled_right = style_string(spec.right_caret, spec.caret_style)
    styled_val = style_string(padded_val, spec.value_style)
    
    spinner_len = length(spec.left_caret) + 2 + max_val_len + 2 + length(spec.right_caret)
    lbl_len = length(spec.label)
    styled_lbl = style_string(spec.label, spec.label_style)
    
    if lbl_len > 0:
        avail_space = max_width - lbl_len - spinner_len
        sep_len = if avail_space >= 2 then avail_space else 2
        line = styled_lbl + spaces(sep_len) + styled_left + "  " + styled_val + "  " + styled_right
        raw_len = lbl_len + sep_len + spinner_len
    else:
        line = styled_left + "  " + styled_val + "  " + styled_right
        raw_len = spinner_len
        
    if raw_len < max_width:
        line = line + spaces(max_width - raw_len)
        
    lines = [line]
    while length(lines) < max_height:
        lines.push(spaces(max_width))
        
    return lines[0:max_height]
```
