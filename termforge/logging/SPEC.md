# LogStreamer Component Specification

Provides scrollable rolling log buffer widgets with auto-highlighting level decorators (INFO, ERROR, WARNING) mapped to theme styles.

## 1. Data Models

### `LogStreamerSpec`
- `max_lines`: integer (buffer limit size)
- `auto_scroll`: boolean (scrolls viewport automatically to bottom on appending logs)
- `timestamp_format`: string (datetime format template, e.g. `"%H:%M:%S"`)
- `level_colors`: dictionary (map from level string to theme style token)
- `buffer`: list of dictionaries (logs state entries, retaining `timestamp`, `level`, and `message`)
- `width`: integer | null
- `height`: integer | null
- `spec_type`: `"log_streamer"`

---

## 2. Rendering & Rolling Buffers

Maintains a fixed rolling queue size by removing oldest items when pushing new entries. Formats timestamps and log level indicators, then truncates messages exceeding viewport width limit constraints.

#### Pseudocode:
```
function log(spec: LogStreamerSpec, level: str, message: str, timestamp: str|null) -> void:
    ts = timestamp if timestamp is not null else current_datetime_string(spec.timestamp_format)
    spec.buffer.push({timestamp: ts, level: level, message: message})
    if length(spec.buffer) > spec.max_lines:
        spec.buffer.remove_first()

function render_log_streamer(spec: LogStreamerSpec, max_width: int, max_height: int) -> list[str]:
    lines = []
    for entry in spec.buffer:
        ts_part = "[" + entry.timestamp + "] " if entry.timestamp is not empty else ""
        level_part = "[" + entry.level + "]"
        prefix_w = length(ts_part) + length(level_part) + 1
        
        # Truncate message if exceeds max width limit
        disp_msg = entry.message
        if prefix_w + length(disp_msg) > max_width:
            allowed = max_width - prefix_w
            if allowed > 1:
                disp_msg = substring(entry.message, 0, allowed - 1) + "…"
            else:
                raw_full = ts_part + level_part + " " + entry.message
                disp_msg = ""
                ts_part = ""
                level_part = substring(raw_full, 0, max_width - 1) + "…"
                
        # Resolve level highlighting colors
        styled_level = level_part
        if entry.level in spec.level_colors:
            styled_level = style_string(level_part, spec.level_colors[entry.level])
            
        if level_part is not empty:
            lines.push(ts_part + styled_level + " " + disp_msg)
        else:
            lines.push(level_part)
            
    if spec.auto_scroll:
        return lines[-max_height:]
    else:
        return lines[0:max_height]
```
