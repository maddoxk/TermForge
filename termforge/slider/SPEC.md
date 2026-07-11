# Slider Component Specification

Provides horizontal range sliders showing numeric progress tracks with custom fill/empty character symbols.

## 1. Data Models

### `SliderSpec`
- `value`: float (current numeric position)
- `min_val`: float (minimum limit, default `0.0`)
- `max_val`: float (maximum limit, default `100.0`)
- `label`: string (description text next to slider)
- `track_fill_char`: string (progress fill symbol, default `"="`)
- `track_empty_char`: string (progress empty track symbol, default `"-"`)
- `handle_char`: string (slider knob knob, default `"●"`)
- `value_format`: string (value formatter text pattern, default `"{val}%"`)
- `track_fill_style`: string | null (theme style token for progress fill)
- `track_empty_style`: string | null (theme style token for empty track)
- `handle_style`: string | null (theme style token for knob handle)
- `value_style`: string | null (theme style token for value text)
- `label_style`: string | null (theme style token for description label)
- `width`: integer | null
- `height`: integer | null
- `spec_type`: `"slider"`

---

## 2. Progress Spacing & Handle Offsets Math

Scales progress tracks to fit remaining width space dynamically. Computes knob offset position proportionally based on values clamped within min/max bounds.

#### Pseudocode:
```
function render_slider(spec: SliderSpec, max_width: int, max_height: int) -> list[str]:
    # value display text
    val_disp = if is_integer(spec.value) then integer(spec.value) else spec.value
    formatted_val = replace(spec.value_format, "{val}", string(val_disp))
    
    lbl_len = length(spec.label)
    val_len = length(formatted_val)
    
    # Track boundaries Math
    sep_len = if lbl_len > 0 then 2 else 0
    fixed_len = lbl_len + sep_len + 2 + 1 + val_len
    
    track_w = max_width - fixed_len
    if track_w < 5:
        track_w = 5
        
    # proportional ratio knob position
    denom = spec.max_val - spec.min_val
    ratio = if denom > 0 then (spec.value - spec.min_val) / denom else 0.0
    ratio = clamp(ratio, 0.0, 1.0)
    
    pos = integer(ratio * (track_w - 1))
    pos = clamp(pos, 0, track_w - 1)
    
    # build segments
    left_fill = repeat(spec.track_fill_char, pos)
    right_empty = repeat(spec.track_empty_char, track_w - 1 - pos)
    
    styled_track = "[" + style(left_fill, spec.track_fill_style) + style(spec.handle_char, spec.handle_style) + style(right_empty, spec.track_empty_style) + "]"
    
    # combine
    styled_lbl = style(spec.label, spec.label_style)
    styled_val = style(formatted_val, spec.value_style)
    
    if lbl_len > 0:
        line = styled_lbl + spaces(sep_len) + styled_track + " " + styled_val
    else:
        line = styled_track + " " + styled_val
        
    actual_len = lbl_len + sep_len + 2 + track_w + 1 + val_len
    if actual_len < max_width:
        line = line + spaces(max_width - actual_len)
        
    lines = [line]
    while length(lines) < max_height:
        lines.push(spaces(max_width))
        
    return lines[0:max_height]
```
