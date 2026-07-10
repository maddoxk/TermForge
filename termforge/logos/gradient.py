from __future__ import annotations
from termforge.core.types import ColorDepth
from termforge.image.ansi import fg_color_ansi, RESET

def get_gradient_color(colors: list[tuple[int, int, int]], t: float) -> tuple[int, int, int]:
    if not colors:
        return (255, 255, 255)
    if len(colors) == 1:
        return colors[0]
        
    t = max(0.0, min(1.0, t))
    num_segments = len(colors) - 1
    scaled_t = t * num_segments
    segment_idx = int(scaled_t)
    segment_idx = min(segment_idx, num_segments - 1)
    local_t = scaled_t - segment_idx
    
    c1 = colors[segment_idx]
    c2 = colors[segment_idx + 1]
    
    r = round(c1[0] + (c2[0] - c1[0]) * local_t)
    g = round(c1[1] + (c2[1] - c1[1]) * local_t)
    b = round(c1[2] + (c2[2] - c1[2]) * local_t)
    return (r, g, b)

def apply_gradient(lines: list[str], colors: list[tuple[int, int, int]], depth: ColorDepth) -> list[str]:
    if not lines or not colors:
        return lines
        
    result_lines = []
    for line in lines:
        line_len = len(line)
        if line_len == 0:
            result_lines.append("")
            continue
            
        colored_chars = []
        for c_idx, char in enumerate(line):
            t = c_idx / (line_len - 1) if line_len > 1 else 0.0
            r, g, b = get_gradient_color(colors, t)
            fg = fg_color_ansi(r, g, b, depth)
            colored_chars.append(f"{fg}{char}")
            
        result_lines.append("".join(colored_chars) + RESET)
    return result_lines

def apply_vertical_gradient(lines: list[str], colors: list[tuple[int, int, int]], depth: ColorDepth) -> list[str]:
    if not lines or not colors:
        return lines
        
    num_rows = len(lines)
    result_lines = []
    for r_idx, line in enumerate(lines):
        t = r_idx / (num_rows - 1) if num_rows > 1 else 0.0
        r, g, b = get_gradient_color(colors, t)
        fg = fg_color_ansi(r, g, b, depth)
        result_lines.append(f"{fg}{line}{RESET}")
    return result_lines
