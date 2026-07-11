# Key-Value Grid Component Specification

Provides aligned, two-column key-value list rendering, designed for displaying system diagnostics, parameters, configurations, and summary cards.

## 1. Data Models

### `KeyValueItemSpec`
- `key`: string
- `value`: string
- `key_style`: string | null (theme color token name)
- `value_style`: string | null (theme color token name)
- `spec_type`: `"keyvalue_item"`

### `KeyValueGridSpec`
- `items`: list of `KeyValueItemSpec` elements
- `separator`: string (default `": "`)
- `key_width`: integer | null (optional override for key column width)
- `width`: integer | null
- `height`: integer | null
- `spec_type`: `"keyvalue_grid"`

---

## 2. Rendering Algorithm

Formatting logic pads key labels dynamically to the longest key in the collection (or respects `key_width`), appends the separator, and truncates values exceeding the maximum canvas boundaries.

#### Pseudocode:
```
function render_keyvalue_grid(spec: KeyValueGridSpec, max_width: int, max_height: int) -> list[str]:
    # 1. Determine key column width
    if spec.key_width is not null:
        key_col_w = spec.key_width
    else:
        key_col_w = max(length(item.key) for item in spec.items)
        
    lines = []
    
    # 2. Render rows
    for item in spec.items:
        # Align key left within key column width
        padded_key = pad_right(item.key, key_col_w)
        
        # Calculate raw character width of row
        raw_len = length(padded_key) + length(spec.separator) + length(item.value)
        
        # Apply truncation if row exceeds maximum width
        val_str = item.value
        if raw_len > max_width:
            allowed_val_w = max_width - length(padded_key) - length(spec.separator)
            if allowed_val_w > 1:
                val_str = substring(val_str, 0, allowed_val_w - 1) + "…"
            else:
                val_str = substring("…", 0, max(0, allowed_val_w))
                
        # Format output line
        line = padded_key + spec.separator + val_str
        lines.append(line)
        
    return substring(lines, 0, max_height)
```
