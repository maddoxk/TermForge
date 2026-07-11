"""TermForge tooltip component renderer."""
from __future__ import annotations

from termforge.core.types import Size, ColorDepth, StyleSpec, ColorValue
from termforge.core.theme import ThemeTokens, resolve_token
from termforge.text.render import style_to_ansi
from termforge.tooltip.types import TooltipSpec


def _style_part(text: str, token: str | None, theme: ThemeTokens | None, depth: ColorDepth) -> str:
    if not token or not theme or depth == ColorDepth.MONOCHROME:
        return text
    token_path = token if token.startswith("colors.") else f"colors.{token}"
    try:
        res = resolve_token(theme, token_path)
        if isinstance(res, ColorValue):
            style = StyleSpec(fg=ColorValue(res.r, res.g, res.b, name=None))
            start, end = style_to_ansi(style, theme, depth)
            return f"{start}{text}{end}"
    except KeyError:
        pass
    return text


def render_tooltip(
    spec: TooltipSpec,
    max_size: Size,
    theme: ThemeTokens | None = None,
    depth: ColorDepth = ColorDepth.TRUECOLOR,
) -> list[str]:
    """Render the Tooltip component to canvas overlay lines.

    Args:
        spec: TooltipSpec containing anchor coordinates and text.
        max_size: Size constraints for the overall canvas.
        theme: Optional theme tokens for style resolution.
        depth: Color depth tier.

    Returns:
        List of rendered lines (equal to max_size.height).
    """
    if max_size.height <= 0 or max_size.width <= 0 or not spec.text:
        return [" " * max_size.width] * max_size.height

    inner_w = len(spec.text)
    box_w = inner_w + 2
    box_h = 3

    # 1. Calculate Positioning
    if spec.placement in ("top", "bottom"):
        # Centered horizontally on anchor
        start_x = spec.anchor_x - (inner_w // 2) - 1
        start_x = max(0, min(start_x, max_size.width - box_w))
        
        ptr_idx = spec.anchor_x - start_x - 1
        ptr_idx = max(0, min(ptr_idx, inner_w - 1))

        if spec.placement == "top":
            start_y = spec.anchor_y - 3
        else:
            start_y = spec.anchor_y + 1
            
        start_y = max(0, min(start_y, max_size.height - box_h))
        
        # Build styled parts
        b_sty = spec.bubble_style
        p_sty = spec.pointer_style
        
        c_tl = _style_part("┌", b_sty, theme, depth)
        c_tr = _style_part("┐", b_sty, theme, depth)
        c_bl = _style_part("└", b_sty, theme, depth)
        c_br = _style_part("┘", b_sty, theme, depth)
        c_h = _style_part("─", b_sty, theme, depth)
        c_v = _style_part("│", b_sty, theme, depth)
        
        styled_text = _style_part(spec.text, b_sty, theme, depth)

        if spec.placement == "top":
            # Pointer in bottom border: ▼
            p_char = _style_part("▼", p_sty, theme, depth)
            
            top_line = c_tl + c_h * inner_w + c_tr
            mid_line = c_v + styled_text + c_v
            bot_line = c_bl + c_h * ptr_idx + p_char + c_h * (inner_w - 1 - ptr_idx) + c_br
        else:
            # Pointer in top border: ▲
            p_char = _style_part("▲", p_sty, theme, depth)
            
            top_line = c_tl + c_h * ptr_idx + p_char + c_h * (inner_w - 1 - ptr_idx) + c_tr
            mid_line = c_v + styled_text + c_v
            bot_line = c_bl + c_h * inner_w + c_br

        box_lines = [top_line, mid_line, bot_line]

    else:
        # Placement is left or right
        if spec.placement == "left":
            start_x = spec.anchor_x - box_w
        else:
            start_x = spec.anchor_x + 1
            
        start_x = max(0, min(start_x, max_size.width - box_w))
        
        start_y = spec.anchor_y - 1
        start_y = max(0, min(start_y, max_size.height - box_h))

        b_sty = spec.bubble_style
        p_sty = spec.pointer_style

        c_tl = _style_part("┌", b_sty, theme, depth)
        c_tr = _style_part("┐", b_sty, theme, depth)
        c_bl = _style_part("└", b_sty, theme, depth)
        c_br = _style_part("┘", b_sty, theme, depth)
        c_h = _style_part("─", b_sty, theme, depth)
        c_v = _style_part("│", b_sty, theme, depth)

        styled_text = _style_part(spec.text, b_sty, theme, depth)

        if spec.placement == "left":
            p_char = _style_part("▶", p_sty, theme, depth)
            top_line = c_tl + c_h * inner_w + c_tr
            mid_line = c_v + styled_text + p_char
            bot_line = c_bl + c_h * inner_w + c_br
        else:
            p_char = _style_part("◀", p_sty, theme, depth)
            top_line = c_tl + c_h * inner_w + c_tr
            mid_line = p_char + styled_text + c_v
            bot_line = c_bl + c_h * inner_w + c_br

        box_lines = [top_line, mid_line, bot_line]

    # 2. Overlay onto canvas lines
    lines = []
    left_space = " " * start_x
    right_space = " " * max(0, max_size.width - start_x - box_w)

    empty_line = " " * max_size.width

    for r in range(max_size.height):
        if start_y <= r < start_y + box_h:
            box_idx = r - start_y
            lines.append(f"{left_space}{box_lines[box_idx]}{right_space}")
        else:
            lines.append(empty_line)

    return lines
