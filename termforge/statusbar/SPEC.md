# StatusBar Component Specification

Provides a bottom information panel featuring left, center, and right alignment blocks (typically for status messages, filenames, and coordinates).

## 1. Data Models

### `StatusSectionSpec`
- `text`: string (the metadata value)
- `style`: string | null (theme token for the section, e.g. `"colors.success"`)

### `StatusBarSpec`
- `left`: list of `StatusSectionSpec` elements
- `center`: list of `StatusSectionSpec` elements
- `right`: list of `StatusSectionSpec` elements
- `separator`: string (the divider between segments inside a group, default `" │ "`)
- `separator_style`: string | null (theme token for delimiter characters)
- `width`: integer | null
- `height`: integer | null
- `spec_type`: `"status_bar"`

---

## 2. Rendering & Alignment Math

Allocates positions for the left, center, and right sections inside `max_width`. If the viewport is too narrow to hold all sections without overlapping, it drops the center section first, followed by truncating right and left segments.

#### Parameters:
- `viewport_w`: integer
- `viewport_h`: integer (typically 1)

#### Pseudocode:
```
function render_status_bar(spec: StatusBarSpec, max_width: int, max_height: int) -> list[str]:
    raw_l, styled_l = render_group(spec.left, spec.separator)
    raw_c, styled_c = render_group(spec.center, spec.separator)
    raw_r, styled_r = render_group(spec.right, spec.separator)
    
    L_len = length(raw_l)
    C_len = length(raw_c)
    R_len = length(raw_r)
    
    if L_len + C_len + R_len <= max_width:
        pos_l = 0
        pos_c = floor((max_width - C_len) / 2)
        pos_c = max(pos_c, L_len)
        pos_r = max_width - R_len
        pos_r = max(pos_r, pos_c + C_len)
        
        space1 = space(pos_c - L_len)
        space2 = space(pos_r - (pos_c + C_len))
        line = styled_l + space1 + styled_c + space2 + styled_r
    else:
        # Overlap: omit center
        if L_len + R_len <= max_width:
            space = space(max_width - L_len - R_len)
            line = styled_l + space + styled_r
        else:
            avail_r = max_width - L_len
            if avail_r > 1:
                # Truncate right
                trunc_r = substring(raw_r, 0, avail_r - 2) + "…"
                line = styled_l + style_string(trunc_r, spec.right[last].style)
            else:
                # Truncate left
                trunc_l = substring(raw_l, 0, max_width - 2) + "…"
                line = style_string(trunc_l, spec.left[0].style)
                
    # Pad to max_width
    raw_w = length_without_ansi(line)
    if raw_w < max_width:
        line = line + space(max_width - raw_w)
        
    return [line]
```
