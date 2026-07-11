# Stepper Component Specification

Provides horizontal progress step flow indicators for setup/installation wizards.

## 1. Data Models

### `StepperSpec`
- `steps`: list of strings (step titles)
- `active_idx`: integer (index of active step)
- `connector`: string (connector separator, default `" -> "`)
- `active_style`: string | null (theme style token for active step)
- `inactive_style`: string | null (theme style token for inactive steps)
- `connector_style`: string | null (theme style token for connectors)
- `width`: integer | null
- `height`: integer | null
- `spec_type`: `"stepper"`

---

## 2. Horizontal wizard flow layout Math

Walks through step title strings, formatting the active index title within square brackets (`[title]`). Connects step items using the formatted connector character block.

#### Pseudocode:
```
function render_stepper(spec: StepperSpec, max_width: int, max_height: int) -> list[str]:
    styled_segments = []
    raw_lens = []
    
    for idx, title in enumerate(spec.steps):
        is_active = (idx == spec.active_idx)
        if is_active:
            raw_text = "[" + title + "]"
            styled_text = style_string(raw_text, spec.active_style)
        else:
            raw_text = title
            styled_text = style_string(raw_text, spec.inactive_style)
            
        styled_segments.push(styled_text)
        raw_lens.push(length(raw_text))
        
    styled_conn = style_string(spec.connector, spec.connector_style)
    line = join_strings(styled_segments, styled_conn)
    
    total_raw_len = sum(raw_lens) + length(spec.connector) * (length(spec.steps) - 1)
    if total_raw_len < max_width:
        line = line + spaces(max_width - total_raw_len)
        
    lines = [line]
    while length(lines) < max_height:
        lines.push(spaces(max_width))
        
    return lines[0:max_height]
```
