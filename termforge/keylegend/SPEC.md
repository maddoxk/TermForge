# KeyLegend Component Specification

Provides formatted keyboard shortcut panels and cheat-sheet legend bars for horizontal footer bars and vertical side information regions.

## 1. Data Models

### `KeyLegendSpec`
- `bindings`: list of `InputBindingSpec` elements (mapping shortcut keys to action descriptions)
- `format`: string template (default `"[ {key} ] {description}"`)
- `spacing`: integer (number of spaces between columns in horizontal layout)
- `key_style`: string | null (theme token for key labels)
- `desc_style`: string | null (theme token for descriptions)
- `orientation`: string (either `"horizontal"` or `"vertical"`)
- `width`: integer | null
- `height`: integer | null
- `spec_type`: `"key_legend"`

---

## 2. Rendering & Truncation Algorithm

Maintains template structure integrity during clipping by subtracting template overhead characters first, ensuring that ANSI styling codes are not sliced or broken.

#### Pseudocode:
```
function _truncate_legend_item(key: str, action: str, format_template: str, avail: int) -> tuple[str, str]:
    # Subtract formatting characters length
    static_len = length(format_template.replace("{key}", "").replace("{description}", ""))
    max_len = avail - static_len
    
    if max_len <= 0:
        return "…", ""
        
    if max_len > length(key):
        # Truncate description, keep key whole
        desc_avail = max_len - length(key)
        return key, truncate_string(action, desc_avail)
    else:
        # Key is too long, clear description, truncate key
        return truncate_string(key, max_len), ""
        
function render_key_legend(spec: KeyLegendSpec, max_width: int, max_height: int) -> list[str]:
    if spec.orientation == "horizontal":
        current_len = 0
        parts = []
        for i, b in enumerate(spec.bindings):
            raw = format(spec.format, b.key, b.action)
            sep_len = spec.spacing if i > 0 else 0
            
            if current_len + sep_len + length(raw) > max_width:
                avail = max_width - current_len - sep_len
                if avail > 0:
                    k, d = _truncate_legend_item(b.key, b.action, spec.format, avail)
                    parts.append(format(spec.format, k, d))
                break
                
            parts.append(raw)
            current_len += sep_len + length(raw)
        return [join(parts, spec.spacing)]
        
    else:
        # Vertical: one line per binding
        lines = []
        for b in spec.bindings:
            raw = format(spec.format, b.key, b.action)
            if length(raw) > max_width:
                k, d = _truncate_legend_item(b.key, b.action, spec.format, max_width)
                lines.append(format(spec.format, k, d))
            else:
                lines.append(raw)
        return substring(lines, 0, max_height)
```
