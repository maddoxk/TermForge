# TermForge Borders Module Specification

This module defines borders, frame styling, title and subtitle insertion, and per-side visibility control.

## 1. Data Structures

### `BorderStyle`
Enum of line rendering characters:
- `SINGLE` (e.g. `┌`, `┐`, `─`, `│`)
- `DOUBLE` (e.g. `╔`, `╗`, `═`, `║`)
- `ROUNDED` (e.g. `╭`, `╮`, `─`, `│`)
- `HEAVY` (e.g. `┏`, `┓`, `━`, `┃`)
- `ASCII` (e.g. `+`, `+`, `-`, `|`)
- `NONE` (spaces)

### `BorderSide`
Describes visibility and custom override.
- `visible`: boolean
- `style_override`: `BorderStyle` | null

### `BorderSpec`
- `style`: `BorderStyle`
- `top`, `right`, `bottom`, `left`: `BorderSide`
- `title`: string | null
- `title_align`: `TextAlign` (from text module)
- `subtitle`: string | null
- `content`: `RenderableSpec` | null

---

## 2. Algorithms

### Frame Rendering (`render_border`)
Draws a box border around a list of content lines.

#### Pseudocode:
```
function render_border(spec: BorderSpec, content_lines: list[string], width: int|null, theme: ThemeTokens|null, unicode: bool) -> list[string]:
    glyphs = get_glyphs_by_style(spec.style, theme, unicode)
    
    left_w = 1 if spec.left.visible else 0
    right_w = 1 if spec.right.visible else 0
    
    if width is not null:
        inner_w = max(0, width - left_w - right_w)
    else:
        inner_w = max_line_width_without_ansi(content_lines)
        width = inner_w + left_w + right_w
        
    lines = []
    
    # Render Top Line
    if spec.top.visible:
        top_line = ""
        if spec.left.visible: top_line = top_line + glyphs.tl
        
        # Center/Align title
        title_text = " " + spec.title + " " if spec.title is not null else ""
        title_w = display_width(title_text)
        if title_w > 0 and title_w <= inner_w:
            remaining = inner_w - title_w
            if spec.title_align == CENTER:
                top_line = top_line + h_line(remaining/2) + title_text + h_line(remaining - remaining/2)
            elif spec.title_align == RIGHT:
                top_line = top_line + h_line(remaining - 1) + title_text + h_line(1)
            else: # LEFT
                top_line = top_line + h_line(1) + title_text + h_line(remaining - 1)
        else:
            top_line = top_line + h_line(inner_w)
            
        if spec.right.visible: top_line = top_line + glyphs.tr
        lines.push(top_line)
        
    # Render Body
    for line in content_lines:
        padded_line = pad_line_to_inner_width(line, inner_w)
        body_line = ""
        if spec.left.visible: body_line = body_line + glyphs.v
        body_line = body_line + padded_line
        if spec.right.visible: body_line = body_line + glyphs.v
        lines.push(body_line)
        
    # Render Bottom Line
    if spec.bottom.visible:
        bot_line = ""
        if spec.left.visible: bot_line = bot_line + glyphs.bl
        
        # Subtitle
        sub_text = " " + spec.subtitle + " " if spec.subtitle is not null else ""
        sub_w = display_width(sub_text)
        if sub_w > 0 and sub_w <= inner_w:
            remaining = inner_w - sub_w
            bot_line = bot_line + h_line(1) + sub_text + h_line(remaining - 1)
        else:
            bot_line = bot_line + h_line(inner_w)
            
        if spec.right.visible: bot_line = bot_line + glyphs.br
        lines.push(bot_line)
        
    return lines
```
