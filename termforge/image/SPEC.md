# TermForge Image Module Specification

This module defines image loading, resizing, half-block Unicode encoding, and ASCII character ramp fallback algorithms.

## 1. Data Structures

### `ImageFidelity`
Enum defining how the image is represented:
- `HALF_BLOCK` = "half_block" — Uses terminal cells containing 2 vertical half-block pixels.
- `ASCII_RAMP` = "ascii_ramp" — Map pixels to brightness levels and output characters.

### `ImageSpec`
- `source`: string (path or URL)
- `width`: integer | null
- `height`: integer | null
- `fidelity`: `ImageFidelity` | null
- `preserve_aspect`: boolean

---

## 2. Algorithms

### Aspect-Ratio Resizing (`resize_for_terminal`)
To scale images appropriately for terminal rendering, we must account for the ~2:1 vertical-to-horizontal ratio of terminal character cells.
- If `half_block` is used, each terminal cell displays 2 pixels vertically (top and bottom), making cell aspect ratio 1:1 in pixels.
- If `ascii_ramp` is used, each terminal cell displays 1 pixel, meaning the display aspect of a pixel is 1:2.

#### Pseudocode:
```
function resize_for_terminal(img_w: int, img_h: int, cols: int|null, rows: int|null, preserve_aspect: bool, half_block: bool) -> tuple[int, int]:
    if cols is null and rows is null:
        cols = 80
        
    if cols is not null and rows is not null:
        w = cols
        h = rows * 2 if half_block else rows
        if preserve_aspect:
            img_aspect = img_w / img_h
            display_aspect = w / h if half_block else w / (h * 2.0)
            if img_aspect > display_aspect:
                # Limit by width
                w = cols
                h = int(w / img_aspect) if half_block else int(w / (2.0 * img_aspect))
            else:
                # Limit by height
                h = rows * 2 if half_block else rows
                w = int(h * img_aspect) if half_block else int(h * img_aspect * 2.0)
        return w, h
        
    if cols is not null:
        w = cols
        img_aspect = img_w / img_h
        h = int(w / img_aspect) if half_block else int(w / (2.0 * img_aspect))
        return w, h
        
    if rows is not null:
        h = rows * 2 if half_block else rows
        img_aspect = img_w / img_h
        w = int(h * img_aspect) if half_block else int(h * img_aspect * 2.0)
        return w, h
```

### Half-Block Unicode Rendering (`render_half_block`)
Each terminal cell has a foreground color (top pixel) and background color (bottom pixel). We use the Unicode half-block character `▀` (U+2580) to render them.
If the top and bottom pixels are identical, we optimize by rendering the full block character `█` (U+2588) using only the foreground color.

#### Pseudocode:
```
function render_half_block(pixels: array of RGB, depth: ColorDepth) -> list[string]:
    lines = []
    height = length(pixels)
    width = length(pixels[0])
    
    for y = 0 to height step 2:
        line_str = ""
        for x = 0 to width - 1:
            top_pixel = pixels[y][x]
            bottom_pixel = pixels[y+1][x] if y+1 < height else Black
            
            fg = resolve_ansi_fg_color(top_pixel, depth)
            bg = resolve_ansi_bg_color(bottom_pixel, depth)
            
            if top_pixel == bottom_pixel:
                line_str = line_str + fg + "█"
            else:
                line_str = line_str + fg + bg + "▀"
        lines.push(line_str + ResetANSI)
    return lines
```

### ASCII Character Ramp Rendering
Luminance is calculated using the formula:
$$Y = 0.299R + 0.587G + 0.114B$$
We map $Y \in [0, 1]$ linearly to a character in a ramp (e.g., `" .:-=+*#%@"`).
- `render_ascii` outputs plain characters.
- `render_ascii_colored` outputs characters with ANSI foreground colors.
