"""TermForge toast component renderer."""
from __future__ import annotations

from termforge.core.types import Size, ColorDepth, StyleSpec, ColorValue
from termforge.core.theme import ThemeTokens, resolve_token
from termforge.text.render import style_to_ansi
from termforge.toast.types import ToastSpec


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


def render_toast(
    spec: ToastSpec,
    max_size: Size,
    theme: ThemeTokens | None = None,
    depth: ColorDepth = ColorDepth.TRUECOLOR,
) -> list[str]:
    """Render the Toast component overlay box to canvas lines.

    Args:
        spec: ToastSpec representing the notification message.
        max_size: Size constraints of the canvas.
        theme: Optional theme tokens.
        depth: Color depth tier.

    Returns:
        List of canvas lines (equal to max_size.height).
    """
    if max_size.height <= 0 or max_size.width <= 0 or not spec.text:
        return [" " * max_size.width] * max_size.height

    # 1. Determine glyph set
    if spec.border_style == "rounded":
        tl, tr, bl, br, h, v = "╭", "╮", "╰", "╯", "─", "│"
    elif spec.border_style == "double":
        tl, tr, bl, br, h, v = "╔", "╗", "╚", "╝", "═", "║"
    else:
        tl, tr, bl, br, h, v = "┌", "┐", "└", "┘", "─", "│"

    # 2. Form content message
    prefix = f"[{spec.toast_type.upper()}]"
    raw_content = f"{prefix} {spec.text}"
    inner_w = len(raw_content)
    box_w = inner_w + 2
    box_h = 3

    # Calculate positioning
    if "right" in spec.position:
        start_x = max_size.width - box_w
    else:
        start_x = 0
    start_x = max(0, min(start_x, max_size.width - box_w))

    if "bottom" in spec.position:
        start_y = max_size.height - box_h
    else:
        start_y = 0
    start_y = max(0, min(start_y, max_size.height - box_h))

    # 3. Apply styles
    # Map type to color tokens
    type_tokens = {
        "success": "success",
        "warning": "warning",
        "error": "danger",
        "info": "primary"
    }
    type_token = type_tokens.get(spec.toast_type.lower(), "primary")
    
    styled_prefix = _style_part(prefix, type_token, theme, depth)
    styled_text = _style_part(spec.text, "secondary", theme, depth)
    
    # Combined middle content (ansi safe)
    mid_content = f"{styled_prefix} {styled_text}"

    # Style borders
    border_style_token = "border"
    s_tl = _style_part(tl, border_style_token, theme, depth)
    s_tr = _style_part(tr, border_style_token, theme, depth)
    s_bl = _style_part(bl, border_style_token, theme, depth)
    s_br = _style_part(br, border_style_token, theme, depth)
    s_h = _style_part(h, border_style_token, theme, depth)
    s_v = _style_part(v, border_style_token, theme, depth)

    # Box lines
    top_line = s_tl + s_h * inner_w + s_tr
    mid_line = s_v + mid_content + s_v
    bot_line = s_bl + s_h * inner_w + s_br

    box_lines = [top_line, mid_line, bot_line]

    # 4. Build output lines with background padding
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
