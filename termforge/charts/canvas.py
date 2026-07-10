from __future__ import annotations
from dataclasses import dataclass, field
from termforge.core.types import ColorDepth, StyleSpec
from termforge.core.theme import ThemeTokens
from termforge.text.render import style_to_ansi

@dataclass
class Canvas:
    width: int
    height: int
    cells: list[list[str]]
    colors: list[list[StyleSpec | None]]

def create_canvas(width: int, height: int, fill: str = " ") -> Canvas:
    cells = [[fill] * width for _ in range(height)]
    colors = [[None] * width for _ in range(height)]
    return Canvas(width=width, height=height, cells=cells, colors=colors)

def set_cell(canvas: Canvas, x: int, y: int, char: str, style: StyleSpec | None = None) -> None:
    # y is from bottom (0 = bottom, height-1 = top) for typical chart plotting
    # but we store in standard row-major (0 = top, height-1 = bottom)
    row = canvas.height - 1 - y
    if 0 <= row < canvas.height and 0 <= x < canvas.width:
        canvas.cells[row][x] = char
        canvas.colors[row][x] = style

def draw_line(canvas: Canvas, x1: int, y1: int, x2: int, y2: int, char: str, style: StyleSpec | None = None) -> None:
    # Bresenham's line algorithm
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    
    while True:
        set_cell(canvas, x1, y1, char, style)
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy

def draw_rect(canvas: Canvas, x: int, y: int, w: int, h: int, char: str, style: StyleSpec | None = None) -> None:
    # Draw bottom/top edges
    for i in range(x, x + w):
        set_cell(canvas, i, y, char, style)
        set_cell(canvas, i, y + h - 1, char, style)
    # Draw left/right edges
    for j in range(y, y + h):
        set_cell(canvas, x, j, char, style)
        set_cell(canvas, x + w - 1, j, char, style)

def canvas_to_lines(canvas: Canvas, theme: ThemeTokens | None, depth: ColorDepth) -> list[str]:
    lines = []
    for r in range(canvas.height):
        row_ansi = []
        for c in range(canvas.width):
            char = canvas.cells[r][c]
            style = canvas.colors[r][c]
            if style:
                start_ansi, end_ansi = style_to_ansi(style, theme, depth)
                row_ansi.append(f"{start_ansi}{char}{end_ansi}")
            else:
                row_ansi.append(char)
        lines.append("".join(row_ansi))
    return lines


@dataclass
class BrailleCanvas:
    width: int # In terminal cells
    height: int # In terminal cells
    pixels: list[list[bool]] # 2*width by 4*height
    styles: list[list[StyleSpec | None]] # 2*width by 4*height

def create_braille_canvas(width: int, height: int) -> BrailleCanvas:
    pixels = [[False] * (2 * width) for _ in range(4 * height)]
    styles = [[None] * (2 * width) for _ in range(4 * height)]
    return BrailleCanvas(width=width, height=height, pixels=pixels, styles=styles)

def set_braille_pixel(canvas: BrailleCanvas, x: int, y: int, active: bool = True, style: StyleSpec | None = None) -> None:
    # y is from bottom (0 = bottom, 4*height - 1 = top)
    row = (4 * canvas.height) - 1 - y
    if 0 <= row < (4 * canvas.height) and 0 <= x < (2 * canvas.width):
        canvas.pixels[row][x] = active
        canvas.styles[row][x] = style

def draw_braille_line(canvas: BrailleCanvas, x1: int, y1: int, x2: int, y2: int, style: StyleSpec | None = None) -> None:
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    
    while True:
        set_braille_pixel(canvas, x1, y1, True, style)
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy

def braille_canvas_to_lines(canvas: BrailleCanvas, theme: ThemeTokens | None, depth: ColorDepth) -> list[str]:
    lines = []
    
    # Map dot (dx, dy) within a 2x4 block to its braille byte offset
    # dx in 0..1, dy in 0..3
    dot_map = {
        (0, 0): 0x01, (0, 1): 0x02, (0, 2): 0x04, (0, 3): 0x40,
        (1, 0): 0x08, (1, 1): 0x10, (1, 2): 0x20, (1, 3): 0x80
    }
    
    for r in range(canvas.height):
        row_ansi = []
        for c in range(canvas.width):
            # 2x4 pixel block starts at:
            # x_pixel = 2 * c
            # y_pixel = 4 * r (rows from top in pixels)
            pixel_val = 0
            cell_style = None
            
            # Count pixels and find most common style in this block
            block_styles = []
            for dy in range(4):
                py = 4 * r + dy
                for dx in range(2):
                    px = 2 * c + dx
                    if canvas.pixels[py][px]:
                        pixel_val |= dot_map[(dx, dy)]
                        if canvas.styles[py][px]:
                            block_styles.append(canvas.styles[py][px])
            
            # Most common style
            if block_styles:
                # Map StyleSpec to a hashable tuple representation
                def style_key(s):
                    fg_val = (s.fg.r, s.fg.g, s.fg.b, s.fg.name) if s.fg else None
                    bg_val = (s.bg.r, s.bg.g, s.bg.b, s.bg.name) if s.bg else None
                    return (fg_val, bg_val, s.bold, s.dim, s.italic, s.underline, s.strikethrough)
                
                counts = {}
                key_to_style = {}
                for style in block_styles:
                    key = style_key(style)
                    counts[key] = counts.get(key, 0) + 1
                    key_to_style[key] = style
                
                best_key = max(counts, key=counts.get)
                cell_style = key_to_style[best_key]
                
            char = chr(0x2800 + pixel_val)
            if cell_style:
                start_ansi, end_ansi = style_to_ansi(cell_style, theme, depth)
                row_ansi.append(f"{start_ansi}{char}{end_ansi}")
            else:
                row_ansi.append(char)
        lines.append("".join(row_ansi))
    return lines
