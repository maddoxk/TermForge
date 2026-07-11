# ToggleSwitch Component Specification

Provides sliders/switch toggles representing boolean ON/OFF states with description labels.

## 1. Data Models

### `ToggleSwitchSpec`
- `label`: string (description text next to toggle switch)
- `state`: boolean (ON state if True, OFF state if False)
- `active_indicator`: string (active check indicator, default `"●"`)
- `inactive_indicator`: string (inactive check indicator, default `"○"`)
- `active_label`: string (active text state label, default `"ON"`)
- `inactive_label`: string (inactive text state label, default `"OFF"`)
- `active_style`: string | null (theme style token for active switch)
- `inactive_style`: string | null (theme style token for inactive switch)
- `label_style`: string | null (theme style token for description text)
- `width`: integer | null
- `height`: integer | null
- `spec_type`: `"toggle_switch"`

---

## 2. Rendering & Label Spacing Math

Renders a switch block of constant width (`2 + length(indicator) + 1 + max(length(active_label), length(inactive_label))`) that wraps the state indicator and label. Aligns switch blocks flush to the right boundary by padding spaces between description labels and switches.

#### Pseudocode:
```
function render_toggle_switch(spec: ToggleSwitchSpec, max_width: int, max_height: int) -> list[str]:
    max_lbl_len = max(length(spec.active_label), length(spec.inactive_label))
    if spec.state:
        body = spec.active_indicator + " " + pad_right(spec.active_label, max_lbl_len)
        style = spec.active_style
    else:
        body = spec.inactive_indicator + " " + pad_right(spec.inactive_label, max_lbl_len)
        style = spec.inactive_style
        
    raw_switch = "[" + body + "]"
    styled_switch = style_string(raw_switch, style)
    styled_label = style_string(spec.label, spec.label_style)
    
    switch_len = length(raw_switch)
    label_len = length(spec.label)
    
    if label_len > 0:
        avail_space = max_width - label_len - switch_len
        if avail_space >= 2:
            sep = spaces(avail_space)
        else:
            sep = "  "
        line = styled_label + sep + styled_switch
        raw_len = label_len + length(sep) + switch_len
    else:
        line = styled_switch
        raw_len = switch_len
        
    if raw_len < max_width:
        line = line + spaces(max_width - raw_len)
        
    lines = [line]
    while length(lines) < max_height:
        lines.push(spaces(max_width))
        
    return lines[0:max_height]
```
