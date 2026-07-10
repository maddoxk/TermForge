# TermForge Text Module Specification

This module defines styled text primitives, markup parsing, text wrapping, and truncation algorithms.

## 1. Data Structures

### `TextSpan`
Represents a contiguous range of text sharing a single styling configuration.
- `text`: string
- `style`: `StyleSpec` (from core) | None

### `TextRun`
A collection of `TextSpan` elements that form a single logical line or text block.
- `spans`: array of `TextSpan`

### `TextAlign`
Enum of alignment options:
- `LEFT` = "left"
- `CENTER` = "center"
- `RIGHT` = "right"

### `TextOverflow`
Enum of behavior when text exceeds max width:
- `CLIP` = "clip"
- `ELLIPSIS` = "ellipsis"
- `WRAP` = "wrap"

### `TextSpec`
JSON-serializable descriptor inheriting from `RenderableSpec`.
- `content`: string | `TextRun`
- `align`: `TextAlign`
- `overflow`: `TextOverflow`
- `max_width`: integer | null
- `max_lines`: integer | null

---

## 2. Algorithms

### Markup Parser (`parse_markup`)
Parses nested markup tags in a string and converts them into a `TextRun`.
Tags supported:
- `[bold]...[/bold]` or `[bold]...[/]`
- `[dim]...[/dim]` or `[dim]...[/]`
- `[italic]...[/italic]` or `[italic]...[/]`
- `[underline]...[/underline]` or `[underline]...[/]`
- `[strikethrough]...[/strikethrough]` or `[strikethrough]...[/]`
- `[fg=color]...[/fg]` (where color is hex like `#ff0000` or standard named colors)
- `[bg=color]...[/bg]`

#### Pseudocode:
```
function parse_markup(text: string) -> TextRun:
    pattern = regex( "(\[/?[a-zA-Z_][a-zA-Z0-9_]*(?:=[^\]]+)?\]|\[/\])" )
    tokens = split_by_regex(text, pattern)
    
    current_style = empty StyleSpec
    style_stack = [current_style]
    spans = []
    
    for token in tokens:
        if token starts with "[" and ends with "]":
            tag = strip_brackets(token)
            if tag starts with "/":
                # End tag or generic pop
                if stack length > 1:
                    pop style_stack
            else:
                # Start tag
                new_style = clone(style_stack.top())
                parse tag_name and tag_value
                apply tag changes to new_style
                push new_style onto style_stack
        else:
            if token is not empty:
                spans.push(TextSpan(token, style_stack.top()))
                
    return TextRun(spans)
```

### Word Wrapping (`wrap_run`)
Wraps a `TextRun` to a specified width in terminal columns, respecting double-width characters (e.g., CJK characters have width 2, standard ASCII width 1).

#### Pseudocode:
```
function wrap_run(run: TextRun, width: int) -> list[TextRun]:
    chars = flatten_spans_to_tuples(run) # list of (char, style)
    lines = []
    current_line = []
    current_w = 0
    
    i = 0
    while i < length(chars):
        char, style = chars[i]
        c_w = get_display_width(char)
        
        if char == "\n":
            lines.push(current_line)
            current_line = []
            current_w = 0
            i = i + 1
            continue
            
        if current_w + c_w > width:
            # Word boundary search (look back for a space)
            split_idx = find_last_space(current_line)
            if split_idx > 0:
                word_part = current_line[split_idx+1:]
                current_line = current_line[0:split_idx]
                lines.push(current_line)
                current_line = []
                current_w = 0
                # Rewind i to process the wrapped word on the next line
                i = i - length(word_part)
            else:
                # Character-level wrap
                if current_line is not empty:
                    lines.push(current_line)
                    current_line = []
                    current_w = 0
                else:
                    # Single character is wider than line, force it
                    current_line.push((char, style))
                    lines.push(current_line)
                    current_line = []
                    current_w = 0
                    i = i + 1
        else:
            current_line.push((char, style))
            current_w = current_w + c_w
            i = i + 1
            
    if current_line is not empty or lines is empty:
        lines.push(current_line)
        
    return reconstruct_text_runs(lines)
```

---

## 3. JSON Serialization Examples

### TextSpec Spec
```json
{
  "spec_type": "text",
  "content": {
    "spans": [
      {
        "text": "Hello ",
        "style": {
          "bold": true,
          "dim": false,
          "italic": false,
          "underline": false,
          "strikethrough": false,
          "fg": {
            "r": 255,
            "g": 0,
            "b": 0,
            "name": "red"
          }
        }
      },
      {
        "text": "World",
        "style": null
      }
    ]
  },
  "align": "center",
  "overflow": "wrap",
  "max_width": 40,
  "max_lines": null
}
```
