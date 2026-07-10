from __future__ import annotations
from termforge.core.types import ColorDepth
from termforge.image.ansi import fg_color_ansi, bg_color_ansi, RESET

def render_half_block(pixels: list[list[tuple[int, int, int]]], depth: ColorDepth) -> list[str]:
    lines = []
    height = len(pixels)
    if height == 0:
        return []
    width = len(pixels[0])
    
    for y in range(0, height, 2):
        line = []
        for x in range(width):
            top = pixels[y][x]
            bottom = pixels[y+1][x] if y+1 < height else (0, 0, 0)
            
            fg = fg_color_ansi(top[0], top[1], top[2], depth)
            bg = bg_color_ansi(bottom[0], bottom[1], bottom[2], depth)
            
            if top == bottom:
                line.append(f"{fg}█")
            else:
                line.append(f"{fg}{bg}▀")
        
        lines.append("".join(line) + RESET)
        
    return lines
