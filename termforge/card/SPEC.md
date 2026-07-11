# Card Component Specification

Provides bordered container card panels wrapping titles, subtitles, and multiline text body blocks.

## 1. Data Models

### `CardSpec`
- `title`: string (optional header title string)
- `subtitle`: string (optional header subtitle string)
- `content`: string (multiline body content block text)
- `border_style`: string (border style identifier, default `"single"`)
- `title_style`: string | null (theme style token for titles)
- `subtitle_style`: string | null (theme style token for subtitles)
- `content_style`: string | null (theme style token for body content)
- `border_style_token`: string | null (theme style token for borders, default `"border"`)
- `width`: integer | null
- `height`: integer | null
- `spec_type`: `"card"`

---

## 2. Border Wrap & Header Embedding Math

Fetches border style characters depending on custom specifications. Formats top borders with embedded title/subtitle blocks. Pads inner content lines to match exact layouts.

#### Pseudocode:
```
function render_card(spec: CardSpec, max_width: int, max_height: int) -> list[str]:
    glyphs = get_border_glyphs(spec.border_style)
    inner_w = max_width - 2
    inner_h = max_height - 2
    
    # 1. Header Line 0
    if spec.title is not empty:
        if spec.subtitle is not empty:
            raw_title = " " + spec.title + " "
            raw_sub = "(" + spec.subtitle + ") "
            styled_title = style_string(raw_title, spec.title_style)
            styled_sub = style_string(raw_sub, spec.subtitle_style)
            styled_lbl = styled_title + styled_sub
            lbl_len = length(raw_title) + length(raw_sub)
        else:
            raw_title = " " + spec.title + " "
            styled_lbl = style_string(raw_title, spec.title_style)
            lbl_len = length(raw_title)
            
        if lbl_len > inner_w - 2:
            styled_lbl = style_string(substring(spec.title, 0, inner_w - 4) + "..", spec.title_style)
            lbl_len = length(spec.title)
            
        left_h = 1
        right_h = inner_w - left_h - lbl_len
        line0 = glyphs.top_left + repeat(glyphs.horizontal, left_h) + styled_lbl + repeat(glyphs.horizontal, right_h) + glyphs.top_right
    else:
        line0 = glyphs.top_left + repeat(glyphs.horizontal, inner_w) + glyphs.top_right
        
    lines = [line0]
    
    # 2. Content Lines
    body_lines = split(spec.content, "\n")
    for r from 0 to inner_h - 1:
        if r < length(body_lines):
            raw_line = substring(body_lines[r], 0, inner_w)
            padded = pad_right(raw_line, inner_w)
            lines.push(glyphs.vertical + style_string(padded, spec.content_style) + glyphs.vertical)
        else:
            lines.push(glyphs.vertical + style_string(spaces(inner_w), spec.content_style) + glyphs.vertical)
            
    # 3. Bottom Line
    lines.push(glyphs.bottom_left + repeat(glyphs.horizontal, inner_w) + glyphs.bottom_right)
    
    return lines[0:max_height]
```
