from __future__ import annotations
from termforge.core.types import Size, Position, ColorDepth, StyleSpec, ColorValue
from termforge.core.theme import ThemeTokens
from termforge.core import FlexDirection
from termforge.windows.types import WindowSpec, PaneSpec, ModalSpec
from termforge.borders.types import BorderSpec, BorderSide, BorderStyle
from termforge.borders.render import render_border, strip_ansi
from termforge.text.render import style_to_ansi

def compose_panes(spec: PaneSpec, available: Size) -> list[tuple[Position, Size, RenderableSpec]]:
    if not spec.children:
        return []
        
    num_children = len(spec.children)
    ratios = spec.ratios
    if ratios is None or len(ratios) != num_children:
        ratios = [1.0] * num_children
        
    total_ratio = sum(ratios)
    gaps_space = spec.gap * (num_children - 1)
    
    results = []
    
    if spec.direction == FlexDirection.ROW:
        rem_w = max(0, available.width - gaps_space)
        curr_x = 0
        for i, child in enumerate(spec.children):
            w = int((ratios[i] / total_ratio) * rem_w)
            # Adjust last child to prevent rounding gaps
            if i == num_children - 1:
                w = available.width - curr_x
            child_size = Size(width=max(1, w), height=available.height)
            child_pos = Position(x=curr_x, y=0)
            results.append((child_pos, child_size, child))
            curr_x += w + spec.gap
            
    else: # FlexDirection.COLUMN
        rem_h = max(0, available.height - gaps_space)
        curr_y = 0
        for i, child in enumerate(spec.children):
            h = int((ratios[i] / total_ratio) * rem_h)
            if i == num_children - 1:
                h = available.height - curr_y
            child_size = Size(width=available.width, height=max(1, h))
            child_pos = Position(x=0, y=curr_y)
            results.append((child_pos, child_size, child))
            curr_y += h + spec.gap
            
    return results

def apply_scroll(lines: list[str], scroll_y: int, viewport_height: int) -> list[str]:
    if len(lines) <= viewport_height:
        return lines + [""] * (viewport_height - len(lines))
    start = max(0, min(scroll_y, len(lines) - viewport_height))
    return lines[start : start + viewport_height]

def z_sort(windows: list[WindowSpec]) -> list[WindowSpec]:
    return sorted(windows, key=lambda w: w.z_index)

def render_window(
    spec: WindowSpec,
    content_lines: list[str],
    theme: ThemeTokens | None = None,
    depth: ColorDepth = ColorDepth.TRUECOLOR
) -> list[str]:
    # Determine window dimensions
    width = spec.width if spec.width is not None else 80
    height = spec.height if spec.height is not None else 24
    
    # Inner dimensions (subtracting border lines)
    # top/bottom = 2, left/right = 2
    inner_w = max(0, width - 2)
    inner_h = max(0, height - 2)
    
    # 1. Apply Scroll to content lines
    scrolled_lines = apply_scroll(content_lines, spec.scroll_y, inner_h)
    
    # 2. Build BorderSpec
    border_spec = BorderSpec(
        style=spec.border_style,
        title=spec.title,
        content=spec.content
    )
    
    # 3. Render the border
    bordered = render_border(border_spec, scrolled_lines, width=width, theme=theme, unicode_supported=True)
    
    # 4. Apply highlight styling to border if focused
    border_color_token = "primary" if spec.focused else "border"
    style = StyleSpec(fg=ColorValue(0, 0, 0, name=f"colors.{border_color_token}"))
    start_ansi, end_ansi = style_to_ansi(style, theme, depth)
    
    if start_ansi:
        # We want to color only the border frame (corners, top, bottom, sides)
        # For simplicity, we can wrap the top line, bottom line, and the side characters of each line.
        # This keeps the content styles completely untouched!
        styled_lines = []
        
        # Top line
        styled_lines.append(f"{start_ansi}{bordered[0]}{end_ansi}")
        
        # Body lines (each has side borders)
        for line in bordered[1:-1]:
            # Left side char is first character, right side is last character (or last after ANSI)
            # Since render_border adds exactly 1 char border on left and right:
            # line starts with left border char and ends with right border char
            if len(line) >= 2:
                # Extract first char and last char
                # Wait, content might have ANSI codes, but the border glyphs are added as plain characters at start/end of the line.
                # So line[0] is left border, line[-1] is right border!
                left_border = line[0]
                right_border = line[-1]
                content = line[1:-1]
                styled_lines.append(f"{start_ansi}{left_border}{end_ansi}{content}{start_ansi}{right_border}{end_ansi}")
            else:
                styled_lines.append(line)
                
        # Bottom line
        if len(bordered) > 1:
            styled_lines.append(f"{start_ansi}{bordered[-1]}{end_ansi}")
        return styled_lines
        
    return bordered
